from unittest import TestCase
from dj.commands.dj import dj
from tests.utils import in_temporary_directory
from dj.application import get_current_application


class CLITestCase(TestCase):

    def test_create_new_app(self):
        with in_temporary_directory():
            application = get_current_application()
            init = application.blueprints.get('init')
            model = application.blueprints.get('model')

            print '* Generating application'
            application.generate(init, {
                'app': 'dummy',
                'description': 'x',
                'author': 'x',
                'email': 'x',
                'version': '0.0.1',
                'django_version': '1.10'
            })
            print '* Testing build/run'
            result = dj.main([
                'run',
                'manage.py',
                'help',
                '--quiet'
            ], standalone_mode=False)
            self.assertTrue('for help on a specific subcommand' in result)

            print '* Testing migration flow'
            result = dj.main([
                'run',
                'manage.py',
                'migrate',
                '--quiet'
            ], standalone_mode=False)
            self.assertTrue('Applying auth.0001_initial' in result)

            result = dj.main([
                'run',
                'manage.py',
                'migrate',
                '--quiet'
            ], standalone_mode=False)
            self.assertTrue('No migrations to apply' in result)

            print '* Testing model generation'
            dj.main(['generate', 'model', 'foo'], standalone_mode=False)

            print '* Testing new migration flow'
            dj.main([
                'run',
                'manage.py',
                'makemigrations',
                '--quiet'
            ], standalone_mode=False)

            result = dj.main([
                'run',
                'manage.py',
                'migrate',
                '--quiet'
            ], standalone_mode=False)
            self.assertTrue('Applying dummy.0001_initial' in result)

            result = dj.main([
                'run',
                'manage.py',
                'migrate',
                '--quiet'
            ], standalone_mode=False)
            self.assertFalse('Applying dummy.0001_initial' in result)
