import click


@click.command()
@click.argument('name')
def get_context(name):
    return {
        'name': name
    }
