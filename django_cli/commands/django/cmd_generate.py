import click
from django_cli.commands.base import BlueprintLoaderCommand


@click.command(cls=BlueprintLoaderCommand)
def command(*args, **kwargs):
    """Generate a code stub using the given blueprint."""
    pass


@command.resultcallback()
def generate(context, application=None, blueprint=None, **kwargs):
    """
    Arguments:
        application: represents current application code
        blueprint: represents the blueprint
    """
    if not application:
        click.fail('Could not locate application')
    if not blueprint:
        click.fail('Could not locate blueprint')

    application.generate(blueprint, context)
