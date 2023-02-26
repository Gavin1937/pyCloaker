
from .libadapter import adapter
from inspect import signature
from enum import IntEnum
from typing import Union
import ctypes

class pyCloakerMode(IntEnum):
    Encrypt = 0
    Decrypt = 1

def pyCloakerModeToCInt(mode:Union[pyCloakerMode,int]) -> ctypes.c_int:
    if isinstance(mode, pyCloakerMode):
        return ctypes.c_int(mode.value)
    elif isinstance(mode, int):
        return ctypes.c_int(mode)

class pyCloakerConfig:
    
    def __init__(self, value:ctypes.c_void_p):
        self.__name__ = 'pyCloakerConfig'
        self.__config_ptr = value
    
    def get(self) -> ctypes.c_void_p:
        return self.__config_ptr

class pyCloakerCString:
    
    def __init__(self, data:ctypes.c_void_p):
        self.__name__ = 'pyCloakerCString'
        self.__data_ptr = data
    
    def get(self) -> ctypes.c_void_p:
        return self.__data_ptr

class pyCloaker:
    
    def __init__(self):
        self.__name__ = 'pyCloaker'
        self.__callback_compiler = ctypes.CFUNCTYPE(
            ctypes.c_void_p, ctypes.c_int
        )
    
    # api
    def makeConfig(self,
        mode:Union[pyCloakerMode,int],
        password:str, filename:str,
        outFilename:str, progressCallbackFn
    ) -> pyCloakerConfig:
        """
        Configure a new Encryption/Decryption
        Param:
            mode                 => pyCloakerMode, Encrypt(0) or Decrypt(1)
            password             => str password
            filename             => str input filename
            outFilename          => str output filename
            progressCallbackFn   => callable callback function for display progress
                                    this function should take one int only.
        """
        
        # checking
        if callable(progressCallbackFn) == False:
            raise Exception('Input progressCallbackFn is not callable.')
        paramlen = len(signature(progressCallbackFn).parameters)
        if paramlen > 1:
            raise Exception('Input progressCallbackFn only can have 1 parameter. Too many parameters.')
        elif paramlen < 1:
            raise Exception('Input progressCallbackFn only can have 1 parameter. Not enough parameter.')
        
        progressCallbackFn_ptr = self.__registerCallback(progressCallbackFn)
        _config_ptr = ctypes.c_void_p(
            adapter.makeConfig(
                pyCloakerModeToCInt(mode),
                ctypes.c_char_p(password.encode('utf-8')),
                ctypes.c_char_p(filename.encode('utf-8')),
                ctypes.c_char_p(outFilename.encode('utf-8')),
                progressCallbackFn_ptr
            )
        )
        return pyCloakerConfig(_config_ptr)
    
    def start(self, config:pyCloakerConfig):
        """
        Start configured Encryption/Decryption
        """
        if self.__typeCheck(config, pyCloakerConfig):
            return pyCloakerCString(adapter.start(config.get()))
    
    def destroyConfig(self, config:pyCloakerConfig):
        """
        Destroy configuration
        """
        if self.__typeCheck(config, pyCloakerConfig):
            adapter.destroyConfig(config.get())
    
    def destroyCString(self, cstring:pyCloakerCString):
        """
        Destroy finished temporary content
        """
        if self.__typeCheck(cstring, pyCloakerCString):
            adapter.destroyCString(cstring.get())
    
    
    # private helper functions
    def __typeCheck(self, obj, type) -> bool:
        if not isinstance(obj, type):
            raise TypeError(
                f'Invalid type, want {type.__name__}, but get {obj.__name__}'
            )
        return True
    
    def __registerCallback(self, callback):
        return self.__callback_compiler(callback)

