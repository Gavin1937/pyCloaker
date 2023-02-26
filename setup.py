from setuptools import setup
from setuptools.command.build_ext import build_ext
from subprocess import check_call, check_output, STDOUT
from pathlib import Path
from shutil import copy, rmtree
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
        copy(buildpath/'release/libadapter.so', libpath)
        
        # avoid double compilation
        # # cleanup build directory
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
    

setup(
    name='pyCloaker',
    author='Gavin1937',
    version='1.0',
    packages=['pyCloaker'],
    cmdclass = {'build_ext': build_cloaker_lib},
    runtime_library_dirs=['Cloaker'],
)
