from setuptools import setup, find_packages

try:
    with open('README.rst', encoding='utf-8') as f:
        readme = f.read()
except FileNotFoundError:
    readme = ''

try:
    with open('CHANGES.rst', encoding='utf-8') as f:
        history = f.read().replace('.. :changelog:', '')
except FileNotFoundError:
    history = ''

setup(
    name="python_clamd",
    version='0.0.1.dev0',
    author="janus-sama",
    author_email="zino4onowori@gmail.com",
    maintainer="janus-sama",
    maintainer_email="zino4onowori@gmail.com",
    keywords="python, clamav, antivirus, scanner, virus, libclamav, clamd",
    description="Updated Clamd is a python interface to Clamd (Clamav daemon).",
    long_description=readme + '\n\n' + history,
    url="https://github.com/janus-sama/python_clamd",
    package_dir={'': 'src'},
    packages=find_packages('src', exclude="tests"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="LGPL-2.1-only",
    zip_safe=True,
    include_package_data=False,
)
