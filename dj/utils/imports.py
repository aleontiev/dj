import textwrap
import ast
import os
import sys


def load_module(path):
    directory = os.path.dirname(path)
    old_sys_path = sys.path
    sys.path = [directory] + old_sys_path
    module_path = path.split('/')[-1]
    if module_path.endswith('.py'):
        module_path = module_path[0:-3]
    module = None
    try:
        module = __import__(
            module_path,
            None,
            None,
            [],
            -1
        )
    finally:
        sys.path = old_sys_path
        return module


