import imp
import os


def load_module(path):
    return imp.load_source(os.path.basename(path), path)
