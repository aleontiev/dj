import click


def yellow(message):
    return click.style(message, fg='yellow', bold=True)


def red(message):
    return click.style(message, fg='red', bold=True)


def green(message):
    return click.style(message, fg='green', bold=True)


def white(message):
    return click.style(message, fg='white', bold=True)


def blue(message):
    return click.style(message, fg='blue', bold=True)


def format_command(a, b='', prefix=''):
    return (
        white(prefix) +
        blue('%s: ' % a) + 
        white(b)
    )
