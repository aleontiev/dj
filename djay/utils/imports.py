import imp
import os


def load_module(filename):
    """Loads a module from anywhere in the system.

    Does not depend on or modify sys.path.
    """
    path, name = os.path.split(filename)
    name, ext = os.path.splitext(name)
    (file, filename, desc) = imp.find_module(name, [path])

    try:
        return imp.load_module(name, file, filename, desc)
    finally:
        if file:
            file.close()
