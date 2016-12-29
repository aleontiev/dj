import filecmp
import tempfile
import shutil
import os
import click
from django_cli.utils.redbaron import merge
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
        if 'app' not in context:
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
                full_file = os.path.join(root, file)
                stat = os.stat(full_file)
                content = render_from_file(full_file, context)
                full_file = strip_extension(render_from_string(full_file, context))
                full_file = full_file.replace(templates_root, temp_dir, 1)
                with open(full_file, 'w') as f:
                    f.write(content)
                os.chmod(full_file, stat.st_mode)

    def merge(self):
        """Merges the rendered blueprint into the application."""
        temp_dir = self.temp_dir
        app_dir = self.application.source_directory
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
                relative_target = target.replace(app_dir, '.')
                action = 'r'
                if (
                    os.path.exists(target)
                    and not filecmp.cmp(source, target, shallow=False)
                ):
                    action = click.prompt(
                        '%s already exists, '
                        '[R]eplace, [s]kip, or [m]erge?' % relative_target,
                        default='r'
                    ).lower()
                    if action not in {'r', 'm', 's'}:
                        action = 'r'

                if action == 's':
                    print 'Skipped %s.' % relative_target
                    continue
                if action == 'r':
                    with open(source, 'r') as source_file:
                        with open(target, 'w') as target_file:
                            target_file.write(source_file.read())
                    print 'Generated %s.' % relative_target
                if action == 'm':
                    with open(target, 'r') as target_file:
                        with open(source, 'r') as source_file:
                            merged_fst = merge(
                                target_file.read(),
                                source_file.read()
                            )
                    with open(target, 'w') as target_file:
                        target_file.write(merged_fst.dumps())

                    print 'Merged %s.' % relative_target
                    raise Exception('merge is not implemented')

