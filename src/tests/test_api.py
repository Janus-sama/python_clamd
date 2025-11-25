#!/usr/bin/env python
# -*- coding: utf-8 -*-
import python_clamd
from io import BytesIO
from contextlib import contextmanager
import tempfile
import shutil
import os
import stat

import pytest

mine = (stat.S_IREAD | stat.S_IWRITE)
other = stat.S_IROTH
execute = (stat.S_IEXEC | stat.S_IXOTH)

FILE_PERMISSIONS = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH


@contextmanager
def mkdtemp(*args, **kwargs):
    temp_dir = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


@pytest.fixture(scope="module")
def clamd_unix_socket():
    socket_path = os.environ.get(
        'CLAMD_UNIX_SOCKET',
        '/var/run/clamav/pyclamd.ctl'
    )
    return python_clamd.ClamdUnixSocket(path=socket_path)


class TestUnixSocket:
    kwargs = {}

    def test_ping(self, clamd_unix_socket):
        assert clamd_unix_socket.ping() == 'PONG'

    def test_version(self, clamd_unix_socket):
        assert clamd_unix_socket.version().startswith("ClamAV")

    def test_reload(self, clamd_unix_socket):
        assert clamd_unix_socket.reload().strip() == 'RELOADING'

    def test_scan_eicar_found(self, clamd_unix_socket):
        with tempfile.NamedTemporaryFile('wb', prefix="python-pyclamd", delete=False) as f:
            f.write(python_clamd.EICAR)
            f.flush()
            # Set permissions
            os.chmod(f.name, FILE_PERMISSIONS)
            file_name = f.name

        expected = {file_name: ('FOUND', 'Win.Test.EICAR_HDB-1')}

        try:
            assert clamd_unix_socket.scan(file_name) == expected
        finally:
            os.remove(file_name)

    def test_scan_unicode_path(self, clamd_unix_socket):
        with tempfile.NamedTemporaryFile('wb', prefix="python-clamd_λ_ü", delete=False) as f:
            f.write(python_clamd.EICAR)
            f.flush()
            os.chmod(f.name, FILE_PERMISSIONS)
            file_name = f.name

        expected = {file_name: ('FOUND', 'Win.Test.EICAR_HDB-1')}

        try:
            assert clamd_unix_socket.scan(file_name) == expected
        finally:
            os.remove(file_name)

    def test_multiscan(self, clamd_unix_socket):
        expected = {}
        with tempfile.TemporaryDirectory(prefix="python-clamd_multi") as d:
            for i in range(3):  # Reduced to 3 for faster testing
                file_path = os.path.join(d, "file" + str(i))
                with open(file_path, 'wb') as f:
                    f.write(python_clamd.EICAR)
                os.chmod(file_path, FILE_PERMISSIONS)
                expected[file_path] = ('FOUND', 'Win.Test.EICAR_HDB-1')

            os.chmod(d, stat.S_IRWXU | stat.S_IRGRP |
                     stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

            assert clamd_unix_socket.multiscan(d) == expected

    def test_instream_eicar_found(self, clamd_unix_socket):
        expected = {'stream': ('FOUND', 'Win.Test.EICAR_HDB-1')}
        assert clamd_unix_socket.instream(
            BytesIO(python_clamd.EICAR)) == expected

    def test_instream_success(self, clamd_unix_socket):
        assert clamd_unix_socket.instream(BytesIO(b"foo bar content")) == {
            'stream': ('OK', None)}

    def test_fdscan(self, clamd_unix_socket):
        with tempfile.NamedTemporaryFile('wb', prefix="python-clamd") as f:
            f.write(python_clamd.EICAR)
            f.flush()
            os.fchmod(f.fileno(), (mine | other))
            expected = {f.name: ('FOUND', 'Eicar-Test-Signature')}

            assert clamd_unix_socket.fdscan(f.name) == expected


class TestUnixSocketTimeout(TestUnixSocket):
    kwargs = {"timeout": 20}


def test_cannot_connect():
    with pytest.raises(python_clamd.ConnectionError):
        python_clamd.ClamdUnixSocket(path="/tmp/404").ping()
