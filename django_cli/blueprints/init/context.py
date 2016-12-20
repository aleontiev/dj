import click
import inflection

@click.command()
@click.argument('name')
@click.option('--class-name')
def get_context(name, class_name):
    return {
        'name': inflection.underscore(name),
        'class_name': class_name or inflection.camelize(name)
    }
