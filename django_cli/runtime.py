import os
from django_cli.utils.system import execute, exists, stdout
from django_cli.utils.style import format_command

PYENV_ROOT = os.path.expanduser('~/.pyenv')


def install_dependencies(update=False):
    if not exists("brew"):
        stdout.write(format_command('Installing', 'brew'))
        execute(
            'ruby -e "$(curl -fsSL '
            'https://raw.githubusercontent.com'
            '/Homebrew/install/master/install',
            verbose=True)
    elif update:
        stdout.write(format_command('Updating', 'brew'))
        execute('brew update', verbose=True)

    if not exists('pyenv'):
        stdout.write(format_command('Installing', 'pyenv'))
        execute('brew install pyenv', verbose=True)
    elif update:
        stdout.write(format_command('Updating', 'pyenv'))
        execute('brew install --upgrade pyenv', verbose=True)


def get_runtime_root(version):
    return os.path.join(
        PYENV_ROOT,
        'versions/%s' % version
    )

def install_runtime(version):
    install_dependencies()
    versions = execute('pyenv versions', capture=True)

    if version not in versions:
        stdout.write(format_command('Installing', version))
        execute(
            'PYTHON_CONFIGURE_OPTS="--enable-shared" '
            'pyenv install %s' % version, verbose=True
        )
        execute(
            '%s/bin/pip install -U virtualenv' % get_runtime_root(version)
        )


def get_major_version(version):
    return '.'.join(version.split('.')[0:2])


def install_virtualenv(virtualenv, directory):
    if not os.path.exists(os.path.join(directory, 'bin/activate')):
        stdout.write(format_command('Creating virtual environment'))
        if not os.path.exists(directory):
            os.makedirs(directory)

        execute('%s %s' % (virtualenv, directory))
        bin_directory = os.path.join(directory, 'bin')
        execute('%s/%s' % (bin_directory, 'pip install -U pip'))
        execute(
            '%s/%s' %
            (
                bin_directory,
                'pip install -U setuptools'
            )
        )


class Runtime(object):

    def __init__(
        self,
        version,
        virtual_directory=None,
        directory=None
    ):
        self.version = version
        self.directory = directory or get_runtime_root(self.version)
        self.virtual_directory = virtual_directory or self.directory

        self._is_virtual = self.virtual_directory != self.directory
        self._is_installed = False

    def _install(self):
        if not self._is_installed:
            if self._is_virtual:
                install_virtualenv(
                    '%s/bin/virtualenv' % self.directory,
                    self.virtual_directory
                )
            else:
                install_runtime(self.version)
            self._is_installed = True

    def execute(self, command, **kwargs):
        self._install()
        return execute('%s/%s' % (self.script_directory, command), **kwargs)

    def create_environment(self, directory):
        self._install()
        return Runtime(
            self.version,
            directory=self.directory,
            virtual_directory=directory,
        )

    @property
    def package_directory(self):
        if not hasattr(self, '_package_directory'):
            self._package_directory = os.path.join(
                self.virtual_directory,
                'lib/python%s/site-packages' % get_major_version(self.version)
            )
        return self._package_directory

    @property
    def script_directory(self):
        if not hasattr(self, '_script_directory'):
            self._script_directory = os.path.join(
                self.virtual_directory,
                'bin'
            )
        return self._script_directory

    @property
    def activate_script(self):
        if not hasattr(self, '_activate_script'):
            self._activate_script = os.path.join(
                self.script_directory,
                'activate'
            )
        return self._activate_script
