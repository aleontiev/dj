import sys
import os

from django_cli.application import get_current_application
import click


class BlueprintLoaderCommand(click.MultiCommand):

    @property
    def application(self):
        if not hasattr(self, '_application'):
            self._application = get_current_application()
        return self._application

    @property
    def blueprints(self):
        if not hasattr(self, '_blueprints'):
            blueprints = self.application.get_blueprints()
            self._blueprints = {
                blueprint.name: blueprint for blueprint in blueprints
            }
        return self._blueprints

    def list_commands(self, context):
        return self.blueprints.keys()

    def get_command(self, context, name):
        return self.blueprints[name].load_context()

    def invoke(self, context):
        args = context.protected_args + context.args
        name = args[0]
        try:
            if name not in self.blueprints:
                context.fail(
                    'Could not find blueprint "%s".' % name
                )
        except Exception as e:
            context.fail(str(e))
        context.params['application'] = self.application
        context.params['blueprint'] = self.blueprints[name]
        return super(BlueprintLoaderCommand, self).invoke(context)


class MultiCommand(click.MultiCommand):

    """MultiCommand that establishes a command hierarchy convention.

    Click commands that use this class can be nested in the following way:

    Directory structure:

        cmd_a.py
        a/
            cmd_b.py
            a1/
                cmd_foo.py
                cmd_bar.py

    Usage:

        a b foo
        a b bar
    """

    COMMAND_NAME = 'command'

    @property
    def parent_module_name(self):
        if not hasattr(self, '_parent_module_name'):
            parts = self.class_module.__name__.split('.')
            self._parent_module_name = '.'.join(parts[0:-1])
        return self._parent_module_name

    @property
    def class_module(self):
        if not hasattr(self, '_class_module'):
            self._class_module = sys.modules[
                self.__class__.__module__
            ]
        return self._class_module

    @property
    def class_filename(self):
        if not hasattr(self, '_class_filename'):
            self._class_filename = self.class_module.__file__
        return self._class_filename

    @property
    def command_name(self):
        if not hasattr(self, '_command_name'):
            name = self.class_filename.split('/')[-1]
            self._command_name = name[4:].split('.')[0]
        return self._command_name

    @property
    def commands_folder(self):
        if not hasattr(self, '_commands_folder'):
            self._commands_folder = os.path.abspath(
                os.path.join(
                    os.path.dirname(self.class_filename),
                    self.command_name
                )
            )
        return self._commands_folder

    @property
    def commands_module_name(self):
        if not hasattr(self, '_commands_module_name'):
            self._commands_module_name = '%s.%s' % (
                self.parent_module_name,
                self.command_name
            )
        return self._commands_module_name

    def list_commands(self, ctx):
        commands = []
        for filename in os.listdir(self.commands_folder):
            if (
                filename.endswith('.py') and
                filename.startswith('cmd_')
            ):
                commands.append(filename[4:-3])
        commands.sort()
        return commands

    def get_command(self, ctx, name):
        # alias-by-prefix support
        all_commands = set(self.list_commands(ctx))
        if name not in all_commands:
            matches = [
                x for x in all_commands if x.startswith(name)
            ]
            if not matches:
                return None
            elif len(matches) > 1:
                print 'Did you mean one of: %s' % ', '.join(sorted(matches))
                return None
            else:
                name = matches[0]

        COMMAND_NAME = self.COMMAND_NAME
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            module_name = '%s.cmd_%s' % (self.commands_module_name, name)
            mod = __import__(
                module_name,
                None,
                None,
                [COMMAND_NAME]
            )
        except ImportError as e:
            print 'Failed to import %s:\n%s' % (module_name, e)
            return
        return getattr(mod, COMMAND_NAME)
