import os
from .addon import Addon
from .generator import Generator

from .utils.imports import parse_setup
from .utils.system import (
    get_directories,
    get_last_touched,
    get_files,
    touch,
    execute
)


class Application(object):

    DEPENDENCY_FILES = [
        'install_requires.txt',
        'dependency_links.txt',
        'setup.py',
        'requirements.txt'
    ]

    def __init__(self):
        self.source_directory = os.getcwd()
        # TODO: generalize this
        self.build_directory = os.path.join(self.source_directory, '.venv')
        self.packages_directory = os.path.join(
            self.build_directory, 'lib/python2.7/site-packages'
        )
        self.activate_script = os.path.join(
            self.build_directory,
            'bin/activate'
        )

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.source_directory)

    @property
    def name(self):
        if not hasattr(self, '_name'):
            name = None
            setup_file = os.path.join(self.source_directory, 'setup.py')
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
                self.source_directory,
                self.name
            )
        return self._application_directory

    def get_addons(self):
        self.build()

        addons = []
        for directory in get_directories(
            self.packages_directory,
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
        return get_last_touched(self.activate_script)

    @property
    def code_last_touched(self):
        # timestamp of last code change
        dependency_files = [
            os.path.join(self.source_directory, file) for file in
            self.DEPENDENCY_FILES
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

    def setup_environment(self):
        if not os.path.exists(self.activate_script):
            print 'Creating virtual environment...'
            try:
                execute('virtualenv %s' % self.build_directory)
            except:
                print 'Failed, try running "pip install virtualenv".'
                raise

    def build(self):
        """Builds the app in a virtual environment.

        Only builds if the build is out-of-date and if the app is non-empty.

        Raises:
            ValidationError if the app fails to build.
        """

        if self.name and self.is_build_outdated:
            self.setup_environment()
            self.execute('pip install -r requirements.txt --process-dependency-links', verbose=True)  # noqa
            touch(self.activate_script)

    def execute(self, command, **kwargs):
        return execute('. %s; %s' % (self.activate_script, command), **kwargs)

    def run(self, command, verbose=True):
        self.build()
        return self.execute(command, verbose=verbose)

    def generate(self, blueprint, context):
        """Generate a blueprint within this application."""
        generator = Generator(self, blueprint, context)
        return generator.generate()

# singleton application instance
current_application = None


def get_current_application():
    global current_application
    if not current_application:
        current_application = Application()
    return current_application
