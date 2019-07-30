import filecmp
import tempfile
import shutil
import os
import click
from dj.utils.codegen import merge
from dj.utils.jinja import strip_extension, render_from_string, render_from_file
from dj.utils.system import stdout as _stdout
from dj.utils import style


class Generator(object):
    def __init__(self, application, blueprint, context, interactive=True, stdout=None):
        self.stdout = stdout or _stdout
        self.application = application
        self.interactive = interactive
        self.blueprint = blueprint
        self.context = context
        self.temp_dir = tempfile.mkdtemp()

    def __del__(self):
        try:
            shutil.rmtree(self.temp_dir)
        finally:
            self.temp_dir = None

    def generate(self):
        """Generate the blueprint."""
        self.render()
        self.merge()

    def render(self):
        """Render the blueprint into a temp directory using the context."""
        context = self.context
        if "app" not in context:
            context["app"] = self.application.name
        temp_dir = self.temp_dir
        templates_root = self.blueprint.templates_directory
        for root, dirs, files in os.walk(templates_root):
            for directory in dirs:
                directory = os.path.join(root, directory)
                directory = render_from_string(directory, context)
                directory = directory.replace(templates_root, temp_dir, 1)
                os.mkdir(directory)
            for file in files:
                full_file = os.path.join(root, file)
                stat = os.stat(full_file)
                content = render_from_file(full_file, context)
                full_file = strip_extension(render_from_string(full_file, context))
                full_file = full_file.replace(templates_root, temp_dir, 1)
                with open(full_file, "w") as f:
                    f.write(content)
                os.chmod(full_file, stat.st_mode)

    def merge(self):
        """Merges the rendered blueprint into the application."""
        temp_dir = self.temp_dir
        app_dir = self.application.directory
        for root, dirs, files in os.walk(temp_dir):
            for directory in dirs:
                directory = os.path.join(root, directory)
                directory = directory.replace(temp_dir, app_dir, 1)
                try:
                    os.mkdir(directory)
                except OSError:
                    pass
            for file in files:
                source = os.path.join(root, file)
                target = source.replace(temp_dir, app_dir, 1)
                relative_target = target.replace(app_dir, ".")
                action = "r"
                if (
                    os.path.exists(target)
                    and not filecmp.cmp(source, target, shallow=False)
                    and os.stat(target).st_size > 0
                ):
                    # target exists, is not empty, and does not
                    # match source
                    if target.endswith("__init__.py"):
                        # default merge __init__.py files
                        # if non-empty, these should only
                        # contain imports from submoduiles
                        action = "m"
                    elif target.endswith("base.py"):
                        # default skip base.py files
                        # these should be extended by the developer
                        action = "s"
                    else:
                        default = "m"
                        action = (
                            click.prompt(
                                style.prompt(
                                    "%s already exists, "
                                    "[r]eplace, [s]kip, or [m]erge?" % (relative_target)
                                ),
                                default=style.default(default),
                            )
                            if self.interactive
                            else default
                        )
                        action = click.unstyle(action).lower()
                        if action not in {"r", "m", "s"}:
                            action = default

                if action == "s":
                    self.stdout.write(
                        "? %s" % style.white(relative_target), fg="yellow"
                    )
                    continue
                if action == "r":
                    with open(source, "r") as source_file:
                        with open(target, "w") as target_file:
                            target_file.write(source_file.read())
                    self.stdout.write(
                        style.green("+ %s" % style.white(relative_target))
                    )
                if action == "m":
                    with open(target, "r") as target_file:
                        with open(source, "r") as source_file:
                            merged = merge(target_file.read(), source_file.read())
                    with open(target, "w") as target_file:
                        target_file.write(merged)

                    self.stdout.write(
                        style.yellow("> %s" % style.white(relative_target))
                    )
