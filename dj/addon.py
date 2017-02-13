import os
from .blueprint import Blueprint


class Addon(object):

    def __init__(self, name, directory):
        self.name = name
        self.module_name = name.replace('-', '_')
        self.directory = directory
        self.blueprints_directory = os.path.join(directory, 'blueprints')

    @property
    def blueprints(self):
        if not hasattr(self, '_blueprints'):
            self._blueprints = {
                b.name: b for b in self.get_blueprints()
            }
        return self._blueprints

    def get_blueprints(self):
        return Blueprint.get_blueprints(
            self.blueprints_directory,
            addon=self
        )

    def __repr__(self):
        return '%s (%s)' % (self.name, self.directory)
