import click
import inflection


@click.command()
@click.argument('name')
@click.option('--help', default=None)
def get_context(name, help):
    name = inflection.underscore(name)
    return {
        'name': name,
        'help': help or name
    }
