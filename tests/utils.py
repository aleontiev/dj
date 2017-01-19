import os
import shutil
import tempfile
from contextlib import contextmanager


@contextmanager
def in_temporary_directory():
    directory = tempfile.mkdtemp()
    cd = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cd)
        shutil.rmtree(directory)
