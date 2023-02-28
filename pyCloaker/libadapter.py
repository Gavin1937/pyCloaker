
__all__ = ['adapter', 'libfilename']

from sys import platform
from pathlib import Path
import ctypes
from site import getsitepackages, getusersitepackages

adapter = None
libfilename = None

# try loading library
try:
    # search for lib
    LIB_BASE = Path('pyCloaker/lib')
    possible_path = ['lib', './pyCloaker/lib', *getsitepackages(), getusersitepackages()]
    possible_name = None
    if platform == 'win32':
        possible_name = ['adapter.dll']
    elif platform == 'linux':
        possible_name = ['libadapter.so']
    possibles_to_check = [Path(i)/j for i in possible_path for j in possible_name]
    
    for pp in possibles_to_check:
        if not pp.exists():
            continue
        LIB_PATH = pp
        break
    
    libfilename = LIB_PATH.name
    if platform == 'win32':
        adapter = ctypes.WinDLL(str(LIB_PATH.resolve()))
    elif platform == 'linux':
        adapter = ctypes.CDLL(str(LIB_PATH.resolve()))
    
    
    # cloaker c adapter api
    # original api reference: Cloaker/gui/cloaker/adapter.h
    
    # void *makeConfig(int, char*, char*, char*, void (*output)(int32_t));
    adapter.makeConfig.argtypes = [
        ctypes.c_int, ctypes.c_char_p,
        ctypes.c_char_p, ctypes.c_char_p,
        ctypes.c_void_p
    ]
    adapter.makeConfig.restype = ctypes.c_void_p
    
    # char *start(void*);
    adapter.start.argtypes = [ctypes.c_void_p]
    adapter.start.restype = ctypes.c_void_p # return void* for compatibility
    
    # void destroyConfig(void*);
    adapter.destroyConfig.argtypes = [ctypes.c_void_p]
    adapter.destroyConfig.restype = ctypes.c_void_p
    
    # void destroyCString(char*);
    adapter.destroyCString.argtypes = [ctypes.c_void_p] # take void* for start() function
    adapter.destroyCString.restype = ctypes.c_void_p
    
except Exception as err:
    raise
