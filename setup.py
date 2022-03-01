import platform
import re
import subprocess
from setuptools import find_packages, setup


# Package meta-data.
NAME = 'cqmore'
VERSION = '1.0'
DESCRIPTION = 'cadquery plugin (under construction)'
URL = 'https://github.com/JustinSDK/cqMore'
EMAIL = 'caterpillar@openhome.cc'
AUTHOR = 'Justin Lin'
LICENSE = 'Apache License 2.0'
REQUIRES_PYTHON = '>=3.6.0'

# What packages are required for this module to be executed?
REQUIRES = [

]

REQUIRES_TEST = [
    'pip',
    'pylint',
    'pytest',
    'pytest-env',
    'pytest-cov',
]

REQUIRES_DEBUG = [

]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}


def has_ssh() -> bool:
    """
    Check that the user has ssh access to github.mmm.com
    First it will verify if ssh is installed in $PATH
    then check if we can authenticate to github.mmm.com
    over ssh. Returns false if either of these are untrue
    """
    result = None
    if 'windows' in platform.platform().lower():
        ssh_test = subprocess.run(['where', 'ssh'])
    else:
        ssh_test = subprocess.run(['which', 'ssh'])
    if ssh_test.returncode == 0:
        result = subprocess.Popen(
            ['ssh', '-Tq', 'git@github.mmm.com', '&>', '/dev/null'])
        result.communicate()
    if not result or result.returncode == 255:
        return False
    return True


def flip_ssh(requires: list) -> list:
    """
    Attempt to authenticate with ssh to github.mmm.com
    If permission is denied then flip the ssh dependencies
    to https dependencies automatically.
    """
    # Not authenticated via ssh. Change ssh to https dependencies
    if not has_ssh():
        requires = list(map(
            lambda x: re.sub(r'ssh://git@', 'https://', x), requires
        ))
    return requires


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=[
            "*.tests",
            "*.tests.*"
            "tests.*",
            "tests"
        ]
    ),
    install_requires=flip_ssh(REQUIRES),
    extras_require={
        'test': flip_ssh(REQUIRES_TEST),
        'debug': flip_ssh(REQUIRES_DEBUG)
    },
    include_package_data=False,
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
