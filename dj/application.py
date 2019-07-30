from __future__ import absolute_import

import os

from .addon import Addon
from .generator import Generator
from .blueprint import Blueprint
from .dependency import DependencyManager, Dependency
from .blueprint import get_core_blueprints
from .utils.system import (
    get_directories,
    get_last_touched,
    find_nearest,
    touch,
    stdout as _stdout
)
from .utils import style
from .config import Config
from .runtime import Runtime
from redbaron import RedBaron


class Application(object):

    def __init__(
        self,
        stdout=None,
        directory=None
    ):
        self.stdout = stdout or _stdout
        current = os.getcwd()
        nearest_setup_file = find_nearest(current, 'setup.py')
        self.directory = directory or (
            os.path.dirname(
                nearest_setup_file
            ) if nearest_setup_file else current
        )
        self.config = Config(self.directory)
        self.setup_file = os.path.join(
            self.directory,
            'setup.py'
        )
        self.requirements_file = os.path.join(
            self.directory,
            self.config.get('requirements')
        )
        self.dev_requirements_file = os.path.join(
            self.directory,
            self.config.get('devRequirements'),
        )
        self.local_requirements_file = os.path.join(
            self.directory,
            self.config.get('localRequirements'),
        )
        self.runtime = Runtime(self.config.get('runtime'))

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.directory)

    @property
    def exists(self):
        if not hasattr(self, '_exists'):
            self._exists = os.path.exists(self.setup_file)
        return self._exists

    @staticmethod
    def parse_application_name(setup_filename):
        """Parse a setup.py file for the name.

        Returns:
            name, or None
        """
        with open(setup_filename, 'rt') as setup_file:
            fst = RedBaron(setup_file.read())
            for node in fst:
                if (
                    node.type == 'atomtrailers' and
                    str(node.name) == 'setup'
                ):
                    for call in node.call:
                        if str(call.name) == 'name':
                            value = call.value
                            if hasattr(value, 'to_python'):
                                value = value.to_python()
                            name = str(value)
                            break
                    if name:
                        break
        return name

    def _get_name(self):
        name = self.config.get('name')
        if name:
            return name

        if self.exists:
            try:
                name = Application.parse_application_name(self.setup_file)
            except Exception:
                name = 'unknown'
            self.config.set('name', name)
            self.config.save()
        return name

    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = self._get_name()
        return self._name

    @property
    def addons(self):
        if not hasattr(self, '_addons'):
            self._addons = {
                a.name: a for a in self.get_addons()
            }
        return self._addons

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

    def refresh(self):
        if hasattr(self, '_name'):
            del self._name
        if hasattr(self, '_blueprints'):
            del self._blueprints
        if hasattr(self, '_addons'):
            del self._addons
        if hasattr(self, '_exists'):
            del self._exists

    @property
    def blueprints(self):
        if not hasattr(self, '_blueprints'):
            self._blueprints = {}
            for b in self.get_blueprints():
                # add by full name, e.g. dj.model
                self._blueprints[b.full_name] = b
                if not b.addon or b.name not in self._blueprints:
                    # for blueprints other that init or core,
                    # add them to the global namespace
                    self._blueprints[b.name] = b
        return self._blueprints

    def get_blueprints(self):
        addons = self.addons.values()
        blueprints = [a.blueprints.values() for a in addons]
        return get_core_blueprints() + [x for s in blueprints for x in s]

    @property
    def requirements_last_modified(self):
        return get_last_touched(self.requirements_file)

    @property
    def dev_requirements_last_modified(self):
        return get_last_touched(self.dev_requirements_file)

    @property
    def local_requirements_last_modified(self):
        return get_last_touched(self.local_requirements_file)

    @property
    def setup_last_modified(self):
        # timestamp of last setup.py change
        return get_last_touched(self.setup_file)

    @property
    def environment(self):
        if not hasattr(self, '_environment'):
            self._environment = self.runtime.create_environment(
                self.config.environment_path
            )
        return self._environment

    def _get_build_token(self, key):
        return os.path.join(
            self.environment.virtual_directory, 'build.%s' % key
        )

    def _build(self, key, last_modified, cmd, verbose=True):
        token = self._get_build_token(key)
        last_built = get_last_touched(token)
        if not last_built or last_built < last_modified:
            self.stdout.write(style.format_command('Building', key))
            result = self.execute(cmd, verbose=False, capture=True)
            if 'pip' in cmd:
                deps = []
                for line in result.split('\n'):
                    splits = line.split(' ')
                    if line.startswith('Successfully installed'):
                        dep = splits[2]
                        dep = '=='.join(dep.rsplit('-', 1))
                        dep = Dependency(dep)
                        deps.append((dep, style.green('+ ')))
                    elif line.startswith('Requirement already satisfied: '):
                        dep = splits[3]
                        dep = Dependency(dep)
                        deps.append((dep, style.yellow('. ')))
                    elif 'Uninstalling' in line:
                        index = line.index('Uninstalling')
                        dep = line[index:].split(' ')[1]
                        dep = ''.join(dep[0:len(dep) - 1])
                        dep = '=='.join(dep.rsplit('-', 1))
                        dep = Dependency(dep)
                        deps.append((dep, style.red('- ')))

                for dep, prefix in sorted(
                    deps,
                    key=lambda x: str(x[0])
                ):
                    self.stdout.write(prefix + dep.to_stdout())
            touch(token)

    def build(self):
        """Builds the app in the app's environment.

        Only builds if the build is out-of-date and is non-empty.
        Builds in 3 stages: requirements, dev requirements, and app.
        pip is used to install requirements, and setup.py is used to
        install the app itself.

        Raises:
            ValidationError if the app fails to build.
        """

        if self.exists:
            self._build(
                'requirements',
                self.requirements_last_modified,
                'pip install -U -r %s' % self.requirements_file
            )
            try:
                self._build(
                    'requirements (dev)',
                    self.dev_requirements_last_modified,
                    'pip install -U -r %s' % self.dev_requirements_file
                )
            except Exception as e:
                if 'No such file' not in str(e):
                    raise e
                self.stdout.write(
                    style.yellow('Could not find dev requirements')
                )
            try:
                self._build(
                    'requirements (local)',
                    self.local_requirements_last_modified,
                    'pip install -U -r %s' % self.local_requirements_file
                )
            except Exception as e:
                if 'No such file' not in str(e):
                    raise e
                self.stdout.write(
                    style.yellow('Could not find local requirements')
                )
            self._build(
                'application',
                self.setup_last_modified,
                'python %s develop' % self.setup_file
            )

    def execute(self, command, **kwargs):
        return self.environment.execute(command, **kwargs)

    def run(self, command, **kwargs):
        self.build()
        self.stdout.write(style.format_command('Running', command))
        return self.execute(command, **kwargs)

    def generate(self, blueprint, context, interactive=True):
        """Generate a blueprint within this application."""
        if not isinstance(blueprint, Blueprint):
            bp = self.blueprints.get(blueprint)
            if not bp:
                raise ValueError('%s is not a valid blueprint' % blueprint)
            blueprint = bp

        self.stdout.write(
            style.format_command(
                'Generating',
                blueprint.full_name
            )
        )
        generator = Generator(
            self,
            blueprint,
            context,
            interactive=interactive
        )
        result = generator.generate()
        if blueprint.name == 'init':
            # try re-setting the name
            self.refresh()
        return result

    def get_dependency_manager(self, dev=False):
        return DependencyManager(
            os.path.join(
                self.directory,
                self.dev_requirements_file if dev else self.requirements_file
            )
        )

    def add(self, addon, dev=False, interactive=True):
        """Add a new dependency and install it."""
        dependencies = self.get_dependency_manager(dev=dev)
        other_dependencies = self.get_dependency_manager(dev=not dev)
        existing = dependencies.get(addon)
        self.stdout.write(style.format_command('Adding', addon))
        dependencies.add(addon)
        try:
            # try running the build
            self.build()
            self.refresh()

            # remove version of this in other requirements file
            other_dependencies.remove(addon, warn=False)

            # run new addon constructor
            constructor_name = '%s.init' % Dependency(addon).module_name
            constructor = self.blueprints.get(constructor_name)

            if constructor:
                context = constructor.load_context().main(
                    [], standalone_mode=False
                )
                self.generate(constructor, context, interactive=interactive)
        except Exception as e:
            # restore original settings
            self.stdout.write(style.red(str(e)))
            self.stdout.write(
                style.yellow('Could not find %s' % addon)
            )
            dependencies.remove(addon)
            if existing:
                dependencies.add(existing)
            return

    def remove(self, addon, dev=False):
        """Remove a dependency and uninstall it."""
        dependencies = self.get_dependency_manager(dev=dev)
        other_dependencies = self.get_dependency_manager(dev=not dev)
        self.stdout.write(style.format_command('Removing', addon))
        removed = dependencies.remove(addon, warn=False)
        if not removed:
            removed = other_dependencies.remove(addon, warn=False)

        if removed:
            self.build()
        else:
            exception = '%s is not installed.' % Dependency(addon).to_stdout()
            self.stdout.write(style.red(exception))

    def info(self):
        output = []
        dev_requirements = self.get_dependency_manager(dev=True).dependencies
        requirements = self.get_dependency_manager(dev=False).dependencies
        app = self.to_stdout()
        if self.exists:
            output.append(style.blue('Application:\n %s' % app))
            if requirements:
                output.append(style.blue('Requirements:'))
                for _, dep in sorted(
                        requirements.items(),
                        key=lambda x: x[0].lower()):
                    output.append(' ' + dep.to_stdout())
            if dev_requirements:
                output.append(style.blue('Requirements (dev):'))
                for _, dep in sorted(
                        dev_requirements.items(),
                        key=lambda x: x[0].lower()
                ):
                    output.append(' ' + dep.to_stdout())
        else:
            output.append(
                style.yellow(
                    '%s, try running %s.' % (
                        app, style.white('dj init')
                    )
                )
            )

        return '\n'.join(output)

    def to_stdout(self):
        return '%s %s %s' % (
            style.white(self.name),
            style.gray('@'),
            style.green(self.runtime.version)
        ) if self.name else style.yellow('No application')

# singleton application instance
current_application = None


def get_current_application():
    global current_application
    if not current_application:
        current_application = Application()
    return current_application


def set_current_application(application):
    global current_application
    current_application = application
