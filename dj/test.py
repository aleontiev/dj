import shutil
import os
from dj.commands.dj import execute
from dj.application import set_current_application, Application
from tempfile import mkdtemp
import multiprocessing


class TemporaryApplication(object):

    DEFAULT_INIT_PARAMS = {
        'app': 'dummy',
        'description': 'dummy',
        'author': 'dummy',
        'email': 'dummy@foo.com',
        'version': '0.0.1',
        'django_version': '1.10'
    }

    def __init__(self, params=None):
        self._params = params or self.DEFAULT_INIT_PARAMS
        self._initialized = False
        self._directory = None
        self._application = None

    def _initialize(self):
        if not self._initialized:
            self._initialized = True
            self._directory = mkdtemp()
            self._application = Application(directory=self._directory)
            set_current_application(self._application)
            # generate initial blueprint
            self._application.generate('init', self._params)

    def __del__(self):
        if self._initialized and self._directory:
            shutil.rmtree(self._directory)
            self._initialized = False
            self._directory = None
            self._application = None
            set_current_application(None)

    def execute(self, command, async=False):
        def _execute(command):
            cd = os.getcwd()
            try:
                os.chdir(self._directory)
                result = execute(command)
                return result
            finally:
                os.chdir(cd)

        self._initialize()
        if async:
            job = multiprocessing.Process(
                target=_execute,
                args=(command, ),
            )
            job.start()
            return job
        else:
            return _execute(command)
