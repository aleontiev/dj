import click
import inflection


@click.command()
@click.argument('name')
def get_context(name):
    """Generate a model with given name.

    You will need to run "dj migrate" to create
    the migration file and apply it to your local
    development database.

    For example:

        dj generate model Foo

        dj migrate
    """
    return {
        'name': inflection.underscore(name),
        'class_name': inflection.camelize(name)
    }
