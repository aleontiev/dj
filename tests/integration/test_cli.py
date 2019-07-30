from __future__ import print_function
from unittest import TestCase
import click
from dj.utils.style import yellow, white
from dj.test import TemporaryApplication
import time
import requests


class CLITestCase(TestCase):

    def log(self, msg):
        print(white('\n*** ') + yellow(msg))

    def test_create_new_app(self):
        application = TemporaryApplication()

        self.log('Testing build')
        result = application.execute('run python manage.py help --quiet')
        self.assertTrue('for help on a specific subcommand' in result, result)

        self.log('Testing lint')
        result = application.execute('run flake8 dummy --quiet')
        self.assertFalse(result)

        self.log('Testing migrate')
        result = application.execute('run python manage.py migrate --quiet')
        self.assertTrue('Applying auth.0001_initial' in result, result)

        result = application.execute('run manage.py migrate --quiet')
        self.assertFalse('Applying auth.0001_initial' in result, result)

        self.log('Testing generate model')
        application.execute('generate model foo --not-interactive')

        # testing fails
        result = application.execute('run pytest --quiet')
        self.assertTrue('no such table: dummy_foo' in result, result)

        application.execute('run manage.py makemigrations --quiet')

        result = application.execute('run manage.py migrate --quiet')
        self.assertTrue('Applying dummy.0001_initial' in result, result)

        result = application.execute('run manage.py migrate --quiet')
        self.assertFalse('Applying dummy.0001_initial' in result, result)

        self.log('Testing test')
        result = application.execute('run pytest --quiet')
        self.assertTrue('1 passed' in result)

        self.log('Testing generate command')
        application.execute('generate command foobar')

        result = application.execute('run manage.py help --quiet')
        self.assertTrue('foobar' in result, result)

        result = application.execute('run manage.py foobar --quiet')
        self.assertTrue('foobar called' in result, result)

        self.log('Testing info')
        result = click.unstyle(application.execute('info'))
        self.assertTrue('Django == 1.10' in result, result)

        self.log('Testing serve')
        server = application.execute(
            'run manage.py runserver 9123 --quiet', run_async=True
        )
        time.sleep(5)

        response = requests.get('http://localhost:9123')
        content = response.content
        self.assertTrue('It worked' in content.decode('utf-8'), content)

        server.terminate()

        self.log('Testing version')
        application.execute('version')
