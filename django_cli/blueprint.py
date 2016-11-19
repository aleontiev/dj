import os
from django_cli.utils.system import get_directories, get_files
from django_cli.utils.imports import load_module


class Blueprint(object):

    @classmethod
    def is_valid(cls, directory):
        # valid if there is a `templates` directory
        # and a `context.py` file
        templates = bool(
            list(get_directories(
                directory,
                filter=lambda x: x.endswith('/templates'),
                depth=1
            ))
        )
        context = bool(
            list(get_files(
                directory,
                filter=lambda x: x.endswith('/context.py'),
                depth=1
            ))
        )
        return templates and context

    def __init__(self, directory):
        self.directory = directory
        self.templates_directory = os.path.join(directory, 'templates')
        self.name = os.path.basename(self.directory)
        self.context = os.path.join(directory, 'context.py')

    def load_context(self):
        return load_module(self.context).get_context

    def __repr__(self):
        return '%s (%s)' % (self.name, self.directory)
