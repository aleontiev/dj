import os
import tempfile


class Generator(object):

    def __init__(self, application, blueprint, context):
        self.application = application
        self.blueprint = blueprint
        self.context = context
        self.temp_dir = tempfile.mkdtemp()

    def __del__(self):
        try:
            os.remove(self.temp_dir)
        finally:
            self.temp_dir = None

    def generate(self):
        """Generate the blueprint."""
        self.render()
        self.merge()

    def render(self):
        """Render the blueprint into a temp directory using the context."""
        pass

    def merge(self):
        """Merges the rendered blueprint into the application."""
        pass
