import os
from django_cli.utils.system import execute, exists

PYENV_ROOT = os.path.expanduser('~/.pyenv')


def install_dependencies(update=False):
    if not exists("brew"):
        print 'Installing brew...'
        execute(
            'ruby -e "$(curl -fsSL '
            'https://raw.githubusercontent.com'
            '/Homebrew/install/master/install',
            verbose=True)
    elif update:
        print 'Updating brew...'
        execute('brew update', verbose=True)

    if not exists('pyenv'):
        print 'Installing pyenv...'
        execute('brew install pyenv', verbose=True)
    elif update:
        print 'Updating pyenv...'
        execute('brew install --upgrade pyenv', verbose=True)

    if not exists('pyenv-virtualenv'):
        print 'Installing pyenv-virtualenv...'
        execute('brew install pyenv-virtualenv', verbose=True)
    elif update:
        print 'Updating pyenv-virtualenv'
        execute('brew install --upgrade pyenv-virtualenv', verbose=True)


def install_runtime(version):
    name = 'django-%s' % version
    install_dependencies()
    versions = execute('pyenv versions', capture=True)

    if version not in versions:
        print 'Installing version %s' % version
        execute("pyenv install %s" % version, verbose=True)

    if name not in versions:
        execute("pyenv virtualenv %s %s" % (version, name), verbose=True)


class Runtime(object):

    def __init__(self, name, version=None, directory=None):
        self.name = name
        self.version = version or name
        self.directory = directory or '%s/versions/%s' % (
            PYENV_ROOT,
            self.name
        )
        self.bin_directory = os.path.join(directory, 'bin')
        self._installed = False

    def _install(self):
        if not self._installed:
            install_runtime(self.version)
            self._installed = True

    def execute(self, command, **kwargs):
        self._install()
        return execute('%s/%s' % (self.bin_directory, command), **kwargs)

    def create_environment(self, directory):
        if not os.path.exists(os.path.join(directory, 'bin/activate')):
            print 'Creating virtual environment...'
            os.makedirs(directory)
            self.execute('virtualenv --clean %s' % directory)
        return Runtime(self.name, version=self.version, directory=directory)
