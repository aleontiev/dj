import os
import sys
from dj.utils.system import get_directories, get_files
from dj.utils.imports import load_module


class Blueprint(object):
    @classmethod
    def is_valid(cls, directory):
        # valid if there is a `templates` directory
        # and a `context.py` file
        templates = bool(
            list(
                get_directories(
                    directory, filter=lambda x: x.endswith("/templates"), depth=1
                )
            )
        )
        context = bool(
            list(
                get_files(
                    directory, filter=lambda x: x.endswith("/context.py"), depth=1
                )
            )
        )
        return templates and context

    @classmethod
    def get_blueprints(cls, directory, addon=None):
        return [
            Blueprint(d, addon=addon)
            for d in get_directories(
                directory, filter=lambda x: cls.is_valid(x), depth=1
            )
        ]

    def __init__(self, directory, addon=None):
        self.directory = directory
        self.addon = addon
        self.templates_directory = os.path.join(directory, "templates")
        self.name = os.path.basename(self.directory)
        self.context = os.path.join(directory, "context.py")

    @property
    def full_name(self):
        return "%s.%s" % (self.addon.name, self.name) if self.addon else self.name

    def load_context(self):
        return load_module(self.context).get_context

    def __repr__(self):
        return "%s (%s)" % (self.name, self.directory)


def get_core_blueprints():
    if getattr(sys, "frozen", False):
        # get blueprints relative to sys.executable
        path = os.path.join(os.path.dirname(sys.executable), "dj/blueprints")
    else:
        # get blueprints folder relative to this file
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "blueprints"))

    blueprints = Blueprint.get_blueprints(path)
    return blueprints
