import os
import click
import six
import sys
import subprocess
import signal


def get_platform_os():
    if not exists("uname"):
        return "Windows"

    return execute("uname -s", capture=True)


def true(x):
    return True


def iser(x):
    def inner(y):
        return x == y
    return inner


def get(directory, filter=None, depth=0, include_files=False, include_dirs=False):
    if isinstance(filter, six.string_types):
        flt = iser(filter)
    if not callable(filter):
        # if filter is None/unsupported type, allow all
        flt = true
    else:
        flt = filter

    for root, dirs, files in os.walk(directory):
        search = []
        if include_files:
            search.extend(files)
        if include_dirs:
            search.extend(dirs)

        for file in search:
            file = os.path.join(root, file)
            if flt(file):
                yield file

        depth -= 1
        if depth == 0:
            break


def get_files(directory, filter=None, depth=0):
    return get(directory, filter, depth, include_files=True)


def get_directories(directory, filter=None, depth=0):
    return get(directory, filter, depth, include_dirs=True)


def get_last_touched(file):
    return os.path.getmtime(file) if os.path.exists(file) else None


def touch(file):
    with open(file, "a"):
        os.utime(file, None)


def make_terminate_handler(process, signal=signal.SIGTERM):
    def inner(*args):
        try:
            os.killpg(os.getpgid(process.pid), signal)
        except OSError:
            pass

    return inner


def execute(command, abort=True, capture=False, verbose=False, echo=False, stream=None):
    """Run a command locally.

    Arguments:
        command: a command to execute.
        abort: If True, a non-zero return code will trigger an exception.
        capture: If True, returns the output of the command.
            If False, returns a subprocess result.
        echo: if True, prints the command before executing it.
        verbose: If True, prints the output of the command.
        stream: If set, stdout/stderr will be redirected to the given stream.
            Ignored if `capture` is True.
    """
    stream = stream or sys.stdout

    if echo:
        out = stream
        out.write(u"$ %s" % command)

    # Capture stdout and stderr in the same stream
    command = u"%s 2>&1" % command

    if verbose:
        out = stream
        err = stream
    else:
        out = subprocess.PIPE
        err = subprocess.PIPE

    process = subprocess.Popen(command, shell=True, stdout=out, stderr=err)
    # propagate SIGTERM to all child processes within
    # the process group. this prevents subprocesses from
    # being orphaned when the current process is terminated
    signal.signal(signal.SIGTERM, make_terminate_handler(process))

    # Wait for the process to complete
    stdout, _ = process.communicate()
    stdout = stdout.strip() if stdout else ""
    if hasattr(stdout, "decode"):
        stdout = stdout.decode("utf-8")

    if abort and process.returncode != 0:
        message = u'Error #%d running "%s"%s' % (
            process.returncode,
            command,
            ":\n====================\n" "%s\n" "====================\n" % (stdout)
            if stdout
            else "",
        )
        raise Exception(message)
    if capture:
        return stdout
    else:
        return process


def find_nearest(directory, filename):
    full_path = os.path.join(directory, filename)
    exists = os.path.exists(full_path)
    if exists:
        return full_path
    if directory == "/":
        return None
    return find_nearest(os.path.abspath(os.path.join(directory, os.pardir)), filename)


def exists(program):
    try:
        execute("command -v %s" % program, verbose=False)
        return True
    except Exception:
        return False


class StyleStdout(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def write(self, message, **kwargs):
        copy = self.kwargs.copy()
        copy.update(kwargs)
        click.echo(click.style(message, **copy))


stdout = StyleStdout(fg="white", bold=True)
