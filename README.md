
# Python API wrapper for [Cloaker](https://github.com/spieglt/Cloaker) library

A Python API wrapper on top of [spieglt/Cloaker](https://github.com/spieglt/Cloaker)'s encryption/decryption library written in Rust

## Dependencies

* [python](https://www.python.org/) version >= 3.8
* [Cloaker](https://github.com/spieglt/Cloaker)

## Compile & Install

* Requirement
  * [git](https://git-scm.com/)
  * [rust](https://www.rust-lang.org/)
  * [cargo](https://doc.rust-lang.org/cargo/)

After you install all the requirements, simply use setup.py to compile and install.

```sh
pip install .

# or build cloaker first to ensure it works

python setup.py build_ext
```

* **Note**
  * This package have sucessfully compiled & installed on Ubuntu 22.04
  * In windows, this package can compile and install, but libadapter.start() may run into problem: "OSError: exception: access violation writing 0x0000000000000000"
  * Other os should be fine but never tested.

## Usage

**Note that this wrapper is strongly typed, so you should carefully check your variable types.**

```py
from pyCloaker import (
    pyCloaker, pyCloakerMode,
    pyCloakerConfig, pyCloakerCString,
    defaultProgressCallbackFn,
    __version__,
)

def callback(percentage):
    print(f'{str(percentage).zfill(3)}%')

print(f'pyCloaker version: {__version__}')

# initialize api
cloaker = pyCloaker()

# create encryption/decryption configuration
mode = pyCloakerMode.Encrypt # or pyCloakerMode.Decrypt
password = '1234'
filename = 'img.jpg'
outFilename = 'outfile'
config:pyCloakerConfig = cloaker.makeConfig(
    mode, password,
    filename, outFilename,
    callback # or leave it empty, makeConfig() will use defaultProgressCallbackFn()
)

# start encryption/decryption
cstr:pyCloakerCString = cloaker.start(config)

# cleanup
cloaker.destroyConfig(config)
cloaker.destroyCString(cstr)
```
