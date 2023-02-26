
__all__ = ['adapter']

from platform import system
from pathlib import Path
import ctypes

adapter = None

# try loading library
try:
    print(Path().resolve())
    LIB_BASE = Path('pyCloaker/lib')
    if not LIB_BASE.exists():
        LIB_BASE = Path('lib')
    if not LIB_BASE.exists():
        raise Exception('Cannot find lib folder in \'./pyCloaker/lib\' or \'./lib\'.')
    if system() == 'Windows':
        LIB_PATH = LIB_BASE / 'adapter.dll'
        if not LIB_PATH.exists():
            LIB_PATH = LIB_BASE / 'libadapter.so'
    else: # other os
        LIB_PATH = LIB_BASE / 'libadapter.so'
    if not LIB_PATH.exists():
        raise Exception('Cannot find libadapter binary.')
    
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
