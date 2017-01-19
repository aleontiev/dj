from django_cli.application import get_current_application
from django_cli.blueprint import get_core_blueprints
from django_cli.utils.system import StyleStdout
from django_cli.utils import style
import click

stdout = StyleStdout()

from .patch import patch_help_formatting
patch_help_formatting()


class BlueprintLoaderCommand(click.MultiCommand):

    @property
    def application(self):
        if not hasattr(self, '_application'):
            self._application = get_current_application()
        return self._application

    @property
    def addons(self):
        if not hasattr(self, '_addons'):
            addons = self.application.get_addons()
            self._addons = {
                addon.name: addon for addon in addons
            }
        return self._addons

    @property
    def blueprints(self):
        if not hasattr(self, '_blueprints'):
            addons = self.addons
            blueprints = {}
            for addon in addons:
                for blueprint in addon.get_blueprints():
                    blueprints[
                        '%s.%s' %
                        (addon.name, blueprint.name)
                    ] = blueprint
            for blueprint in get_core_blueprints():
                blueprints[blueprint.name] = blueprint

            self._blueprints = blueprints
        return self._blueprints

    def list_commands(self, context):
        return self.blueprints.keys()

    def get_command(self, context, name):
        return self.blueprints[name].load_context()

    def invoke(self, context):
        args = context.protected_args + context.args
        name = args[0]
        stdout.write(
            style.format_command(
                'Generating',
                '%s %s' % (
                    name,
                    args[1] if len(args) > 1 else ''
                )
            )
        )

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

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

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
                stdout.write(
                    'Did you mean one of: %s' %
                    ', '.join(
                        sorted(matches)))
                return None
            else:
                name = matches[0]

        return self.commands.get(name)
