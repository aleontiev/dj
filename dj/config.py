import os
import yaml


class Config(object):

    """A singleton for reading and writing configuration."""
    instances = {}
    defaults = {
        'requirements': 'requirements.txt',
        'devRequirements': 'requirements.txt.dev',
        'localRequirements': 'requirements.txt.local',
        'runtime': 'system'
    }
    filename = 'dj.yml'
    build_directory = 'build'

    def __new__(cls, file):
        if not Config.instances.get(file):
            Config.instances[file] = Config.__Config(file)
        return Config.instances[file]

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    @classmethod
    def get_environment_path(cls, directory):
        return os.path.join(
            directory,
            cls.build_directory
        )

    class __Config(object):

        def __init__(self, directory):
            self.directory = directory
            self.file = os.path.join(
                directory,
                Config.filename
            )
            self._data = {}
            self._load()

        def set(self, key, value):
            self._data[key] = value

        def clear(self, key):
            self._data.pop(key, None)

        def clear_all(self, prefix=''):
            for key in self._data.keys():
                if key.startswith(prefix):
                    self._data.pop(key)

        def get(self, key, default=None):
            return self._data.get(key, default)

        @property
        def environment_path(self):
            return Config.get_environment_path(self.directory)

        def save(self):
            """Save current settings to config file."""
            try:
                self._dump()
            except IOError:
                self._create()
                self._dump()

        def _load(self):
            """Load config file into memory."""
            try:
                with open(self.file, 'r') as file:
                    self._data = yaml.load(file)
            except IOError:
                # no config file
                pass
            except yaml.YAMLError as err:
                raise Exception(
                    'Could not parse corrupt config file: %s\n'
                    'Try running "rm %s"' % (
                        str(err),
                        self.file,
                    )
                )
            # set defaults
            for key, value in Config.defaults.items():
                if key not in self._data:
                    self._data[key] = value

        def _create(self):
            """Create config file if it does not exist."""
            path = os.path.dirname(self.file)
            if not os.path.exists(path):
                os.makedirs(path)

        def _dump(self):
            with open(self.file, 'w') as file:
                yaml.dump(
                    self._data,
                    file,
                    encoding='utf-8',
                    allow_unicode=True,
                    default_flow_style=False
                )
