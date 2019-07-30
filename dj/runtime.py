import os

from dj.utils.system import execute, exists, stdout, get_platform_os
from dj.utils.style import format_command

PYENV_ROOT = os.path.expanduser("~/.pyenv")


def install_pyenv_dependencies(update=False):
    platform = get_platform_os()
    if platform == "Darwin":
        if not exists("brew"):
            stdout.write(format_command("Installing", "brew"))
            execute(
                'ruby -e "$(curl -fsSL '
                "https://raw.githubusercontent.com"
                "/Homebrew/install/master/install",
                verbose=True,
            )
        elif update:
            stdout.write(format_command("Updating", "brew"))
            execute("brew update", verbose=True)

        if not exists("pyenv"):
            stdout.write(format_command("Installing", "pyenv"))
            execute("brew install pyenv", verbose=True)
        elif update:
            stdout.write(format_command("Updating", "pyenv"))
            execute("brew install --upgrade pyenv", verbose=True)
    elif platform == "Linux":
        if not exists("curl"):
            stdout.write(format_command("Installing", "curl"))
            execute("sudo apt-get install curl")
        if not exists("pyenv"):
            stdout.write(format_command("Installing", "pyenv"))
            execute(
                "curl -L "
                "https://github.com/pyenv/pyenv-installer/"
                "raw/master/bin/pyenv-installer"
                "| bash"
            )
        elif update:
            stdout.write(format_command("Updating", "pyenv"))
            execute("pyenv update", verbose=True)


def get_runtime_root(version):
    if version == "system":
        return None

    return os.path.join(PYENV_ROOT, "versions/%s" % version)


def install_runtime(version):
    if version == "system":
        # use system python version
        if "virtualenv" not in execute("pip list", capture=True):
            execute("pip install -U virtualenv")

    else:
        # use pyenv to manage versions
        install_pyenv_dependencies()
        versions = execute("pyenv versions", capture=True)
        root = get_runtime_root(version)

        if version not in versions:
            stdout.write(format_command("Installing", version))
            execute(
                'PYTHON_CONFIGURE_OPTS="--enable-shared" ' "pyenv install %s" % version,
                verbose=True,
            )

        if "virtualenv" not in execute("%s/bin/pip list" % root, capture=True):
            execute("%s/bin/pip install -U virtualenv" % root)


def get_major_system_version():
    version = execute("python -V", capture=True).split(" ")[-1]
    return get_major_version(version)


def get_major_version(version):
    if version == "system":
        return get_major_system_version()
    return ".".join(version.split(".")[0:2])


def install_virtualenv(virtualenv, directory):
    if not os.path.exists(os.path.join(directory, "bin/activate")):
        # stdout.write(format_command('Creating virtual environment'))
        if not os.path.exists(directory):
            os.makedirs(directory)

        execute("%s %s" % (virtualenv, directory))
        bin_directory = os.path.join(directory, "bin")
        execute("%s/%s" % (bin_directory, "pip install -U pip"))
        execute("%s/%s" % (bin_directory, "pip install -U setuptools"))


class Runtime(object):
    def __init__(self, version, virtual_directory=None, directory=None):
        self.version = version
        self.directory = directory or get_runtime_root(self.version)
        self.virtual_directory = virtual_directory or self.directory

        self._is_virtual = self.virtual_directory != self.directory
        self._is_installed = False

    def _install(self):
        if not self._is_installed:
            if self._is_virtual:
                install_virtualenv(
                    ("%s/bin/virtualenv" % self.directory)
                    if self.directory
                    else "virtualenv",
                    self.virtual_directory,
                )
            else:
                install_runtime(self.version)
            self._is_installed = True

    def execute(self, command, **kwargs):
        self._install()
        env = kwargs.pop("env", {})
        env = " ".join(('%s="%s"' % (k, v) for k, v in env.items()))
        env = "%s " % env if env else ""
        return execute("%s%s/%s" % (env, self.script_directory, command), **kwargs)

    def create_environment(self, directory):
        self._install()
        return Runtime(
            self.version, directory=self.directory, virtual_directory=directory
        )

    @property
    def package_directory(self):
        if not hasattr(self, "_package_directory"):
            self._package_directory = os.path.join(
                self.virtual_directory,
                "lib/python%s/site-packages" % get_major_version(self.version),
            )
        return self._package_directory

    @property
    def script_directory(self):
        if not hasattr(self, "_script_directory"):
            self._script_directory = os.path.join(self.virtual_directory, "bin")
        return self._script_directory

    @property
    def activate_script(self):
        if not hasattr(self, "_activate_script"):
            self._activate_script = os.path.join(self.script_directory, "activate")
        return self._activate_script
