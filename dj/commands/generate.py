from __future__ import absolute_import
import click
from jinja2.exceptions import UndefinedError
from dj.application import get_current_application


class GenerateCommand(click.MultiCommand):

    @property
    def application(self):
        if not hasattr(self, '_application'):
            self._application = get_current_application()
        return self._application

    def list_commands(self, context):
        return self.application.blueprints.keys()

    def get_command(self, context, name):
        return self.application.blueprints[name].load_context()

    def invoke(self, context):
        args = context.protected_args + context.args
        name = args[0]
        application = self.application
        blueprint = application.blueprints.get(name)
        if not application:
            raise click.ClickException('Could not locate application')
        if not blueprint:
            raise click.ClickException('Could not locate blueprint')

        command = self.get_command(context, name)
        args = args[1:]
        ctx = command.main(args, standalone_mode=False)

        try:
            return application.generate(blueprint, ctx)
        except UndefinedError as e:
            raise click.ClickException(
                '%s.\n'
                "The blueprint's context may be invalid." % str(e)
            )


@click.command(cls=GenerateCommand)
def generate(*args, **kwargs):
    """Generate a code stub."""
    pass
