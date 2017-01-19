import click
import inflection


@click.command()
@click.argument('name')
def get_context(name):
    return {
        'name': inflection.underscore(name),
        'class_name': inflection.camelize(name)
    }
