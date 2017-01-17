from __future__ import absolute_import

import os
import click
from .addon import Addon
from .generator import Generator
from .dependencies import DependencyManager
from .utils.imports import parse_setup
from .utils.system import (
    get_directories,
    get_last_touched,
    get_files,
    touch,
)
from .utils.style import format_command
from .config import Config
from .runtime import Runtime
from .utils.system import stdout as _stdout


class Application(object):

    VIRTUAL_ENV_NAME = 'build'

    def __init__(
        self,
        stdout=None,
        directory=None
    ):
        self.stdout = stdout or _stdout
        self.directory = directory or os.getcwd()
        self.config = Config(self.directory)

        self.setup_file = 'setup.py'
        self.requirements = self.config.get('requirements')
        self.dev_requirements = self.config.get('devRequirements')
        self.dependency_files = (
            self.requirements,
            self.dev_requirements,
            self.setup_file,
        )
        runtime = self.config.get('runtime')
        self.runtime = Runtime(runtime)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.directory)

    @property
    def name(self):
        if not hasattr(self, '_name'):
            name = None
            setup_file = os.path.join(self.directory, self.setup_file)
            if os.path.exists(setup_file):
                try:
                    name = parse_setup(setup_file)['name']
                except Exception as e:
                    import traceback
                    raise Exception(
                        'Failed to parse app setup file: %s\n%s' %
                        (str(e), traceback.format_exc())
                    )
            self._name = name
        return self._name

    @property
    def application_directory(self):
        if not hasattr(self, '_application_directory'):
            self._application_directory = os.path.join(
                self.directory,
                self.name
            )
        return self._application_directory

    def get_addons(self):
        self.build()

        addons = []
        for directory in get_directories(
            self.environment.package_directory,
            filter=lambda x: x.endswith('/blueprints')
        ):
            parent_directory = '/'.join(directory.split('/')[0:-1])
            name = os.path.basename(parent_directory)
            addons.append(Addon(name, parent_directory))
        return addons

    def get_blueprints(self):
        blueprints = [a.get_blueprints() for a in self.get_addons()]
        return [x for s in blueprints for x in s]

    @property
    def build_last_touched(self):
        # timestamp of last build
        return get_last_touched(self.environment.activate_script)

    @property
    def code_last_touched(self):
        # timestamp of last code change
        dependency_files = [
            os.path.join(self.directory, file) for file in
            self.dependency_files
        ]
        code_files = list(get_files(
            self.application_directory,
            lambda x: x.endswith('.py'),
        ))
        return max([
            get_last_touched(file) for file in code_files + dependency_files
        ])

    @property
    def is_build_outdated(self):
        build_last_touched = self.build_last_touched
        code_last_touched = self.code_last_touched
        return not build_last_touched or build_last_touched < code_last_touched

    @property
    def environment(self):
        if not hasattr(self, '_environment'):
            self._environment = self.runtime.create_environment(
                self.config.environment_path
            )
        return self._environment

    def build(self):
        """Builds the app in the app's environment.

        Only builds if the build is out-of-date and if the app is non-empty.

        Raises:
            ValidationError if the app fails to build.
        """

        if self.name and self.is_build_outdated:
            self.stdout.write(format_command('Building'))
            self.execute('pip install -r %s -r %s' % (
                self.requirements,
                self.dev_requirements
            ), verbose=True)
            touch(self.environment.activate_script)

    def execute(self, command, **kwargs):
        return self.environment.execute(command, **kwargs)

    def run(self, command, **kwargs):
        self.build()
        return self.execute(command, **kwargs)

    def generate(self, blueprint, context):
        """Generate a blueprint within this application."""
        generator = Generator(self, blueprint, context)
        return generator.generate()

    def add(self, addon, dev=False):
        """Add a new dependency and install it."""
        dependencies = DependencyManager(
            os.path.join(
                self.directory,
                self.dev_requirements if dev else self.requirements
            )
        )
        dependencies.add(addon)
        self.build()

# singleton application instance
current_application = None


def get_current_application():
    global current_application
    if not current_application:
        current_application = Application()
    return current_application
