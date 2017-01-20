from unittest import TestCase
import click
from dj.commands.dj import execute
from tests.utils import in_temporary_directory
from dj.application import get_current_application


class CLITestCase(TestCase):

    def test_create_new_app(self):
        with in_temporary_directory():
            application = get_current_application()

            print '* Generating application'
            application.generate('init', {
                'app': 'dummy',
                'description': 'x',
                'author': 'x',
                'email': 'x',
                'version': '0.0.1',
                'django_version': '1.10'
            })
            print '* Testing build/run'
            result = execute('run manage.py help --quiet')
            self.assertTrue('for help on a specific subcommand' in result)

            print '* Testing migration flow'
            result = execute('run manage.py migrate --quiet')
            self.assertTrue('Applying auth.0001_initial' in result)

            result = execute('run manage.py migrate --quiet')
            self.assertTrue('No migrations to apply' in result)

            print '* Testing model generation'
            execute('generate model foo')
            application.generate('model', {
                'name': 'foo',
                'class_name': 'Foo'
            })

            print '* Testing new migration flow'
            execute('run manage.py makemigrations --quiet')

            result = execute('run manage.py migrate --quiet')
            self.assertTrue('Applying dummy.0001_initial' in result)

            result = execute('run manage.py migrate --quiet')
            self.assertFalse('Applying dummy.0001_initial' in result)

            application.generate('command', {
                'name': 'foobar',
                'help': 'Foo'
            })

            result = execute('run manage.py help --quiet')
            self.assertTrue('foobar' in result)

            result = execute('run manage.py foobar --quiet')
            self.assertTrue('foobar called' in result)

            result = click.unstyle(execute('info'))
            self.assertTrue('Django == 1.10' in result)
