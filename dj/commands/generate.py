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
        given_args = context.protected_args + context.args
        interactive = True
        args = []
        for arg in given_args:
            if arg == '--interactive':
                interactive = True
            elif arg == '--not-interactive':
                interactive = False
            else:
                args.append(arg)

        name = args[0]
        application = self.application
        if not application:
            raise click.ClickException('Could not locate application')

        blueprint = application.blueprints.get(name)
        if not blueprint:
            raise click.ClickException('Could not locate blueprint')

        command = blueprint.load_context()
        args = args[1:]
        ctx = command.main(args, standalone_mode=False)

        try:
            return application.generate(
                blueprint,
                ctx,
                interactive=interactive
            )
        except UndefinedError as e:
            raise click.ClickException(
                '%s.\n'
                "The blueprint's context may be invalid.\n"
                'Blueprint: %s\n'
                'Context: %s' % (str(e), str(blueprint), str(ctx))
            )


@click.command(cls=GenerateCommand)
@click.option(
    '--interactive/--not-interactive',
    default=True
)
def generate(*args, **kwargs):
    """Generate a code stub."""
    pass
