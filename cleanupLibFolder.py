
from pathlib import Path
from shutil import rmtree

if __name__ == "__main__":
    print('Cleaning up \'./pyCloaker/lib\' folder...')
    
    libpath = Path('./pyCloaker/lib')
    if libpath.exists() == False:
        raise Exception('Cannot find folder: \'./pyCloaker/lib\'.')
    
    build = libpath/'build'
    Cloaker = libpath/'Cloaker'
    Cargo_lock = libpath/'Cargo.lock'
    rmtree(build, ignore_errors=True)
    rmtree(Cloaker, ignore_errors=True)
    Cargo_lock.unlink(missing_ok=True)
