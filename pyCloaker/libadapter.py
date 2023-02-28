
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
    suffix = None
    if platform == 'win32':
        suffix = '.dll'
    elif platform == 'linux':
        suffix = '.so'
    for pp in possible_path:
        pp = Path(pp)
        
        lib = [i for i in pp.rglob('*adapter'+suffix) if i.is_file()]
        if len(lib) < 1:
            raise Exception('Cannot find libadapter binary.')
        else:
            LIB_PATH = lib[0]
            break
    
    libfilename = LIB_PATH.name
    adapter = ctypes.cdll.LoadLibrary(LIB_PATH)
    
    
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
