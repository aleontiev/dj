from unittest import TestCase
from dj.commands.dj import dj
from dj.commands.generate import generate
from tests.utils import in_temporary_directory


class CLITestCase(TestCase):

    def test_create_new_app(self):
        with in_temporary_directory():
            generate.main([
                'init',
                'dummy',
                '--description=x',
                '--author=x',
                '--email=x',
                '--version=0.0.1',
                '--django-version=1.10'
            ], standalone_mode=False)
            result = dj.main(
                ['run', 'manage.py', 'help'],
                standalone_mode=False)

            self.assertEquals(result, '')
