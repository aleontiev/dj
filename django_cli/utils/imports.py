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


def parse_setup(setup_filename):
    """Parse setup.py and return args and keywords args to its setup
    function call

    """
    mock_setup = textwrap.dedent('''\
    def setup(*args, **kwargs):
        __setup_calls__.append((args, kwargs))
    ''')
    parsed_mock_setup = ast.parse(mock_setup, filename=setup_filename)
    with open(setup_filename, 'rt') as setup_file:
        parsed = ast.parse(setup_file.read())
        for index, node in enumerate(parsed.body[:]):
            if (
                not isinstance(node, ast.Expr) or
                not isinstance(node.value, ast.Call) or
                node.value.func.id != 'setup'
            ):
                continue
            parsed.body[index:index] = parsed_mock_setup.body
            break

    fixed = ast.fix_missing_locations(parsed)
    codeobj = compile(fixed, setup_filename, 'exec')
    local_vars = {}
    global_vars = {'__setup_calls__': []}
    exec(codeobj, global_vars, local_vars)
    return global_vars['__setup_calls__'][0][1]
