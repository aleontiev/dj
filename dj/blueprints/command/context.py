import click
import inflection


@click.command()
@click.argument("name")
@click.option("--doc")
def get_context(name, doc):
    """Generate a command with given name.
    The command can be run immediately after generation.

    For example:

        dj generate command bar

        dj run manage.py bar
    """
    name = inflection.underscore(name)
    return {"name": name, "doc": doc or name}
