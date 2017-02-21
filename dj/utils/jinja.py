from jinja2 import Environment, StrictUndefined


def strip_extension(string):
    if string.endswith('.j2'):
        string = string[:-3]
    return string


def render_from_string(string, context):
    environment = Environment(undefined=StrictUndefined)
    return environment.from_string(string).render(**context)


def render_from_file(file, context):
    with open(file, 'r') as f:
        string = f.read()
    return render_from_string(string, context)
