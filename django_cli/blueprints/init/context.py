import click
import inflection
import os


@click.command()
@click.argument('name')
@click.option('--description', prompt='Description', default='N/A')
@click.option('--author', prompt='Author name',
              default=lambda: os.environ.get('USER', ''))
@click.option('--email', prompt='Author email',
              default=lambda: os.environ.get('USER', '') + '@me.com')
@click.option('--version', prompt='Version', default='0.0.1')
@click.option('--django-version', prompt='Django version', default='1.10')
def get_context(name, description, author, email, version, django_version):
    return {
        'app': inflection.underscore(name),
        'description': description,
        'author': author,
        'email': email,
        'version': version,
        'django_version': django_version
    }
