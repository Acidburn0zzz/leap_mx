# -*- coding: utf-8 -*-
# setup.py
# Copyright (C) 2013 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
setup file for leap.mx
"""
import os
import re
from setuptools import setup, find_packages
from setuptools import Command

from pkg.utils.reqs import parse_requirements, is_develop_mode

import versioneer
versioneer.versionfile_source = 'src/leap/mx/_version.py'
versioneer.versionfile_build = 'leap/mx/_version.py'
versioneer.tag_prefix = ''  # tags are like 1.2.0
versioneer.parentdir_prefix = 'leap.mx-'

trove_classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: No Input/Output (Daemon)',
    'Framework :: Twisted',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3'
    ' or later (AGPLv3+)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Communications :: Email',
    'Topic :: Security :: Cryptography',
]

DOWNLOAD_BASE = ('https://github.com/leapcode/leap_mx/'
                 'archive/%s.tar.gz')
_versions = versioneer.get_versions()
VERSION = _versions['version']
VERSION_FULL = _versions['full']
DOWNLOAD_URL = ""

# get the short version for the download url
_version_short = re.findall('\d+\.\d+\.\d+', VERSION)
if len(_version_short) > 0:
    VERSION_SHORT = _version_short[0]
    DOWNLOAD_URL = DOWNLOAD_BASE % VERSION_SHORT

cmdclass = versioneer.get_cmdclass()


class freeze_debianver(Command):
    """
    Freezes the version in a debian branch.
    To be used after merging the development branch onto the debian one.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        proceed = str(raw_input(
            "This will overwrite the file _version.py. Continue? [y/N] "))
        if proceed != "y":
            print("He. You scared. Aborting.")
            return
        template = r"""
# This file was generated by the `freeze_debianver` command in setup.py
# Using 'versioneer.py' (0.7+) from
# revision-control system data, or from the parent directory name of an
# unpacked source archive. Distribution tarballs contain a pre-generated copy
# of this file.

version_version = '{version}'
version_full = '{version_full}'
"""
        templatefun = r"""

def get_versions(default={}, verbose=False):
        return {'version': version_version, 'full': version_full}
"""
        subst_template = template.format(
            version=VERSION_SHORT,
            version_full=VERSION_FULL) + templatefun
        with open(versioneer.versionfile_source, 'w') as f:
            f.write(subst_template)


cmdclass["freeze_debianver"] = freeze_debianver

if os.environ.get("VIRTUAL_ENV", None):
    data_files = None
else:
    # XXX use a script entrypoint for mx instead, it will
    # be automatically
    # placed by distutils, using whatever interpreter is
    # available.
    data_files = [("/usr/local/bin/", ["pkg/mx.tac"])]


requirements = parse_requirements()

if is_develop_mode():
    print
    print ("[WARNING] Skipping leap-specific dependencies "
           "because development mode is detected.")
    print ("[WARNING] You can install "
           "the latest published versions with "
           "'pip install -r pkg/requirements-leap.pip'")
    print ("[WARNING] Or you can instead do 'python setup.py develop' "
           "from the parent folder of each one of them.")
    print
else:
    requirements += parse_requirements(
        reqfiles=["pkg/requirements-leap.pip"])

setup(
    name='leap.mx',
    version=VERSION,
    cmdclass=cmdclass,
    url="http://github.com/leapcode/leap_mx",
    download_url=DOWNLOAD_URL,
    license='AGPLv3+',
    author='The LEAP Encryption Access Project',
    author_email='info@leap.se',
    maintainer='Kali Kaneko',
    maintainer_email='kali@leap.se',
    description=("An asynchronous, transparently-encrypting remailer "
                 "for the LEAP platform"),
    long_description=(
        "An asynchronous, transparently-encrypting remailer "
        "using BigCouch/CouchDB and PGP/GnuPG, written in Twisted Python."
    ),
    namespace_packages=["leap"],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    test_suite='leap.mx.tests',
    tests_require=parse_requirements(
        reqfiles=['pkg/requirements-testing.pip']),
    install_requires=requirements,
    classifiers=trove_classifiers,
    data_files=data_files
)
