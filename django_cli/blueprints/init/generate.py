import click

@click.command()
@click.argument('--name')
@click.option('--class-name')
def generate(context):
    return context
