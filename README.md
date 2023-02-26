
# Python API wrapper for spieglt/Cloaker (github.com/spieglt/Cloaker) library

A Python API wrapper on top of [spieglt/Cloaker](https://github.com/spieglt/Cloaker)'s encryption/decryption library written in Rust

## Dependencies

* [Cloaker](https://github.com/spieglt/Cloaker)

## Compile & Install

* Requirement
  * [git](https://git-scm.com/)
  * [rust](https://www.rust-lang.org/)
  * [cargo](https://doc.rust-lang.org/cargo/)

After you have all the requirements installed, simply run setup.py to compile and install.

```sh
pip install setup.py
```

## Usage

**Note that this wrapper is strongly typed, so you should carefully check your variable types.**

```py
from pyCloaker import (
    pyCloaker, pyCloakerMode,
    pyCloakerConfig, pyCloakerCString
)

def callback(percentage):
    print(f'{str(percentage).zfill(3)}%')

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
    callback
)

# start encryption/decryption
cstr:pyCloakerCString = cloaker.start(config)

# cleanup
cloaker.destroyConfig(config)
cloaker.destroyCString(cstr)
```
