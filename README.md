# clamd

## About
`python_clamd` is a modernized Python wrapper for the [ClamAV](https://www.clamav.net/) anti-virus engine.  
It allows you to interact with a running `clamd` daemon on **Linux, macOS, and Windows**.

This project is a fork of `python-clamd` (last updated 2014), itself a fork of `pyClamd` v0.2.0 by Philippe Lagadec, which in turn extended `pyClamd` v0.1.1 by Alexandre Norman.

### Why this fork?
- Updated for **Python 3.12+ compatibility** (replaced deprecated `pkg_resources` with `importlib.metadata`).  
- Added **type hints and annotations** for better IDE/autocomplete and `mypy` support.  
- Actively maintained with patches and modernization.  

---

## Usage

### Connect via Unix socket
```python
import python_clamd
cd = python_clamd.ClamdUnixSocket()
cd.ping()         # 'PONG'
cd.version()      # 'ClamAV ...'
cd.reload()       # 'RELOADING'
```

### Scan a file
```python
open('/tmp/EICAR','wb').write(python_clamd.EICAR)
cd.scan('/tmp/EICAR')
# {'/tmp/EICAR': ('FOUND', 'Eicar-Test-Signature')}
```

### Scan a stream
```python
from io import BytesIO
cd.instream(BytesIO(python_clamd.EICAR))
# {'stream': ('FOUND', 'Eicar-Test-Signature')}
```

## Installation
### Python package

Coming soon via PyPI:
```python
pip install python-clamd
```

### ClamAV daemon
On Ubuntu:
```bash
sudo apt-get install clamav-daemon clamav-freshclam clamav-unofficial-sigs
sudo freshclam
sudo service clamav-daemon start
```

## Supported Versions
* [x] Python 3.9 – 3.13
* [ ] Python 2.x (dropped)

## License
Released under the LGPL license.

## Contributing
PRs and issues are welcome. This fork exists to keep ClamAV bindings usable on modern Python.
