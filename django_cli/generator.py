import tempfile
import shutil
import os
import click
from django_cli.utils.jinja import (
    strip_extension,
    render_from_string,
    render_from_file
)


class Generator(object):

    def __init__(self, application, blueprint, context):
        self.application = application
        self.blueprint = blueprint
        self.context = context
        self.temp_dir = tempfile.mkdtemp()

    def __del__(self):
        try:
            shutil.rmtree(self.temp_dir)
        finally:
            self.temp_dir = None

    def generate(self):
        """Generate the blueprint."""
        self.render()
        self.merge()

    def render(self):
        """Render the blueprint into a temp directory using the context."""
        context = self.context
        context['app'] = self.application.name
        temp_dir = self.temp_dir
        templates_root = self.blueprint.templates_directory
        for root, dirs, files in os.walk(templates_root):
            for directory in dirs:
                directory = os.path.join(root, directory)
                directory = render_from_string(directory, context)
                directory = directory.replace(templates_root, temp_dir, 1)
                os.mkdir(directory)
            for file in files:
                content = render_from_file(os.path.join(root, file), context)
                file = os.path.join(root, file)
                file = strip_extension(render_from_string(file, context))
                file = file.replace(templates_root, temp_dir, 1)
                with open(file, 'w') as f:
                    f.write(content)

    def merge(self):
        """Merges the rendered blueprint into the application."""
        temp_dir = self.temp_dir
        app_dir = self.application.directory
        for root, dirs, files in os.walk(temp_dir):
            for directory in dirs:
                directory = os.path.join(root, directory)
                directory = directory.replace(temp_dir, app_dir, 1)
                try:
                    os.mkdir(directory)
                except OSError:
                    pass
            for file in files:
                source = os.path.join(root, file)
                target = source.replace(temp_dir, app_dir, 1)
                action = 'r'
                if os.path.exists(target):
                    action = click.prompt(
                        '%s already exists, '
                        '[r]eplace, [s]kip, or [m]erge?' % target,
                        default='r'
                    ).lower()
                    if action not in {'r', 'm', 's'}:
                        action = 'r'
                if action == 'r':
                    with open(source, 'r') as source_file:
                        with open(target, 'w') as target_file:
                            target_file.write(source_file.read())
