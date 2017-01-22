import click
import inflection
import os


def default(txt):
    return click.style(txt, fg='white', bold=True)


def prompt(txt):
    return click.style(txt, fg='green')


@click.command()
@click.argument('name')
@click.option(
    '--description',
    prompt=prompt('Description'),
    default=default('N/A')
)
@click.option(
    '--author',
    prompt=prompt('Author name'),
    default=lambda: default(os.environ.get('USER', ''))
)
@click.option(
    '--email',
    prompt=prompt('Author email'),
    default=lambda: default(os.environ.get('USER', '') + '@me.com')
)
@click.option('--version', prompt=prompt('Version'), default=default('0.0.1'))
@click.option(
    '--django-version', prompt=prompt('Django version'),
    default=default('1.10'))
def get_context(name, description, author, email, version, django_version):
    name = click.unstyle(name)
    description = click.unstyle(description)
    email = click.unstyle(email)
    author = click.unstyle(author)
    version = click.unstyle(version)
    django_version = click.unstyle(django_version)
    return {
        'app': inflection.underscore(name),
        'description': description,
        'author': author,
        'email': email,
        'version': version,
        'django_version': django_version
    }
