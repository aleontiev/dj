import os
from .blueprint import Blueprint
from django_cli.utils.system import get_directories


class Addon(object):

    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.blueprints_directory = os.path.join(directory, 'blueprints')

    def get_blueprints(self):
        blueprints = [
            Blueprint(directory)
            for directory in
            get_directories(
                self.blueprints_directory,
                filter=lambda x: Blueprint.is_valid(x),
                depth=1
            )
        ]
        return blueprints

    def __repr__(self):
        return '%s (%s)' % (self.name, self.directory)
