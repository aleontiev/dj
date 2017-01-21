import os
from .blueprint import Blueprint


class Addon(object):

    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.blueprints_directory = os.path.join(directory, 'blueprints')

    def blueprints(self):
        if not hasattr(self, '_blueprints'):
            self._blueprints = {
                b.name: b for b in self.get_blueprints()
            }
        return self._blueprints

    def get_blueprints(self, directory):
        return Blueprint.get_blueprints(directory, addon=self)

    def __repr__(self):
        return '%s (%s)' % (self.name, self.directory)
