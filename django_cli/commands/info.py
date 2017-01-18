import click
from django_cli.application import get_current_application
from django_cli.utils.style import white, blue
from django_cli.utils.system import stdout


@click.command()
def info():
    """Display info."""
    application = get_current_application()
    dev_requirements = application.get_dependency_manager(
        dev=True
    ).dependencies
    requirements = application.get_dependency_manager(dev=False).dependencies
    if requirements:
        stdout.write(
            blue('Requirements:\n') +
            '\n'.join(
                (
                    ' ' + white(str(dep)) for dep in requirements.values() if not dep.name == '-e .'
                )
            )
        )
    if dev_requirements:
        stdout.write(
            blue('Dev requirements:\n') +
            '\n'.join(
                (
                    ' ' + white(str(dep)) for dep in dev_requirements.values() if not dep.name == '-e .'
                )
            )
        )
