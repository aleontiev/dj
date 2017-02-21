from unittest import TestCase
import click
from dj.test import TemporaryApplication
import time
import requests


class CLITestCase(TestCase):

    def test_create_new_app(self):
        print '* Generating application'
        application = TemporaryApplication()

        print '* Testing build/run'
        result = application.execute('run manage.py help --quiet')
        self.assertTrue('for help on a specific subcommand' in result, result)

        print '* Testing migration flow'
        result = application.execute('run manage.py migrate --quiet')
        self.assertTrue('Applying auth.0001_initial' in result, result)

        result = application.execute('run manage.py migrate --quiet')
        self.assertTrue('No migrations to apply' in result, result)

        print '* Testing model generation'
        application.execute('generate model foo --not-interactive')

        try:
            result = application.execute('test --ds=tests.settings')
        except Exception as e:
            e = click.unstyle(str(e))
            self.assertTrue(
                'no such table: %s_%s' % ('dummy', 'foo') in e,
                e
            )

        print '* Testing new migration flow'
        application.execute('run manage.py makemigrations --quiet')

        application.execute('test --ds=tests.settings')

        result = application.execute('run manage.py migrate --quiet')
        self.assertTrue('Applying dummy.0001_initial' in result, result)

        result = application.execute('run manage.py migrate --quiet')
        self.assertFalse('Applying dummy.0001_initial' in result, result)

        print '* Testing command generation'
        application.execute('generate command foobar')

        result = application.execute('run manage.py help --quiet')
        self.assertTrue('foobar' in result, result)

        result = application.execute('run manage.py foobar --quiet')
        self.assertTrue('foobar called' in result, result)

        result = click.unstyle(application.execute('info'))
        self.assertTrue('Django == 1.10' in result, result)

        print '* Testing server'
        server = application.execute('serve 9123', async=True)
        time.sleep(2)

        response = requests.get('http://localhost:9123')
        content = response.content
        self.assertTrue('It worked' in content, content)

        server.terminate()
