from setuptools import setup
from setuptools.command.build_ext import build_ext
from subprocess import check_call, check_output, STDOUT
from pyCloaker import libfilename
from pathlib import Path
from shutil import copy, rmtree
from sys import platform 
import distutils.sysconfig
from copy import deepcopy
import re


class build_cloaker_lib(build_ext):
    
    description = 'build Rust library spieglt/Cloaker into C shared library.'
    
    def run(self):
        self.__check_deps()
        libpath = Path('./pyCloaker/lib').resolve()
        repopath = libpath / 'Cloaker'
        buildpath = libpath / 'build'
        tomlpath = libpath / 'Cargo.toml'
        if buildpath.exists() == False:
            buildpath.mkdir()
        
        # clone library if not exists
        if repopath.exists() == False:
            check_call([
                'git', 'clone', '--recursive',
                'https://github.com/spieglt/Cloaker.git',
                str(repopath)
            ])
        
        # compile library
        check_call([
            'cargo', 'build', '--release',
            '--manifest-path', str(tomlpath),
            '--target-dir', str(buildpath)
        ])
        
        # copy dll out
        dllpath = buildpath/'release'
        if platform == 'win32':
            dllpath = deepcopy([i for i in dllpath.rglob(libfilename)][0])
        elif platform == 'linux':
            dllpath = deepcopy([i for i in dllpath.rglob(libfilename)][0])
        copy(dllpath, libpath)
        
        # avoid double compilation
        # cleanup build directory
        # rmtree(buildpath)
        
        build_ext.run(self)
    
    def __check_deps(self):
        pattern = r'.*(\d+\.\d+\.\d+).*'
        # check git
        try:
            out = check_output(['git', '--version'], stderr=STDOUT).decode('utf-8')
            mout = re.match(pattern, out)
            if mout is None:
                raise Exception('Cannot find git in current machine.')
        except Exception as err:
            raise
        # check cargo
        try:
            out = check_output(['cargo', '--version'], stderr=STDOUT).decode('utf-8')
            mout = re.match(pattern, out)
            if mout is None:
                raise Exception('Cannot find cargo in current machine.')
        except Exception as err:
            raise
        # check rust
        try:
            out = check_output(['rustc', '--version'], stderr=STDOUT).decode('utf-8')
            mout = re.match(pattern, out)
            if mout is None:
                raise Exception('Cannot find rust in current machine.')
        except Exception as err:
            raise

# get descriptions
description = 'Python API wrapper for Cloaker library'
long_description = ''
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

# load __version__.py
version = {}
with open('./pyCloaker/__version__.py', 'r', encoding='utf-8') as file:
    exec(file.read(), version)

if platform == 'win32':
    data_files = [(distutils.sysconfig.get_python_lib(),[f'pyCloaker/lib/{libfilename}'])]
    package_data = {'pyCloaker':[f'pyCloaker/lib/{libfilename}']}
elif platform == 'linux':
    data_files = [(distutils.sysconfig.get_python_lib(),[f'pyCloaker/lib/{libfilename}'])]
    package_data = {'pyCloaker':[f'pyCloaker/lib/{libfilename}']}


# package settings
setup(
    name='pyCloaker',
    author='Gavin1937',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Gavin1937/pyCloaker',
    version=version['__version__'],
    packages=['pyCloaker'],
    cmdclass = {'build_ext': build_cloaker_lib},
    data_files=data_files,
    package_data=package_data,
    runtime_library_dirs=['Cloaker'],
)
