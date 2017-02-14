import click
import inflection


@click.command()
@click.argument('name')
@click.option('--doc')
def get_context(name, doc):
    name = inflection.underscore(name)
    return {
        'name': name,
        'doc': doc or name
    }
