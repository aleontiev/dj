Django CLI
==========

Django CLI is a command-line tool that automates the repetitive workflows necessary
to manage Django application code:

* Setting up a new project 
* Adding dependencies to the project
* Running the project in an isolated environment
* Generating code stubs

# Why Django CLI?

While there are existing tools that address some of these workflows at the language and framework level
(django-admin/cookiecutter/virtualenv/Makefile),
each tool has its own learning curve, and there are few integration points between them.
The reality of this ecosystem is often an uncertain and boilerplate developer experience, especially
for newcomers. 

Django CLI, insipred by Ember CLI, attempts to fill these gaps by providing a simple, comprehensive, and extendable
interface for the Django development lifecycle. Django CLI is built in Python and provides familiar integration
points for Python developers.

# Getting Started

## Installation

To install Django CLI, simply run [the appropriate installer](./INSTALLERS.md) for your operating system.
Django CLI distributes with PyInstaller and runs within an isolated Python environment.

## Commands

Run `django --help` to see a list of supported commands.
Run `django SUBCOMMAND --help` for help on any specific subcommand:

### django init

Sets up a shell Django project in the current directory.
This command will prompt for all optional arguments, unless passed in.

### django install ADDON[@VERSION]

Imports a Django CLI addon or PyPi package into the current project.

If `--dev` is passed, the addon will only be required for testing and local development.
Otherwise, the addon will be treated as a core package dependency.

In the case of a CLI addon, the addon's initializer will be executed.

### django generate [ADDON.]BLUEPRINT [...ARGS]

Generates a module given a blueprint. The blueprint can be prefixed by the name
of an addon and may take several arguments.

The following core blueprints are supported:

* model NAME

### django run COMMAND [...ARGS]

Run any Django command in development mode.

A virtual environment will be used to build and run the app.
The current system version of Python will be used.

# Developing Addons

It is easy to turn an existing Python or Django library into a Django-CLI addon.
The only distinction is a `blueprints` module within the application package.
This blueprints module should provide all of the addon's blueprints, including an optional
`init` blueprint that is run at installation time.

## Blueprints

Blueprints allows addons to establish structural conventions for
their implementions through the code generation features built into Django-CLI.

A blueprint is a Python package with a `generate.py` module that describes the input
and a `templates` folder that describes the output.

### generate.py

A blueprint's `generate` package should export a single method called `get_context` that serves as a `click`
entrypoint for the blueprint. This entrypoint should describe the required and optional parameters using
`click` decorators and should return the context that will be called by Django CLI's generation methods.

Example:

```
import click

@click.command()
@click.argument('name')
@click.option('--class-name')
def get_context(name, class_name):
    return {
        'name': name,
        'class_name': class_name or name.title()
    }
```

### templates

A blueprint's templates folder contains `Jinja` template files that are rendered and merged into an existing
application when the blueprint is called.

#### rendering

Blueprints are rendered by applying the context passed to Django CLI's `generate` method to each of the files
in the `templates` directory. In addition, file names containing double-underscore delimited variables are replaced by values
from the context. The "app" variable is automatically populated by Django CLI with the name of the current application.

For example, the model blueprint:
```
/
    __app__/
        models/
            __init__.py
                # cli: merge
                from .{{ name }} import {{ class_name }}
            __name__.py
                from django.db import models
                class {{ class_name }}(models.Model):
                    pass
```

Might be rendered as follows for app "foo" and name "bar":

```
/
    foo/
        models/
            __init__.py
                # cli: merge
                from .bar import Bar
            bar.py
                from django.db import models
                class Bar(models.Model):
                    pass
```

#### merging

After a blueprint has been rendered, it is merged into the current application folder by folder.
The following rules are used for each folder:

* Folders and files in the blueprint that do not already exist within an application are created
* Files within the blueprint that do exist and match exactly are ignored
* For files within the blueprint that do not match:
  * If the blueprint file does not contain the `cli: merge` directive, the user will be prompted to replace the file during generation
  * If the blueprint does contain the `cli: merge` directive, the two files will be merged together statement by statement:
    * Import statements that match exactly are only rendered once
    * Assignment statements that match exactly are only rendered once
    * Assignment statements to the same variable with different list/set/dict-type values have their values merged

For example, suppose that app "foo" has the following structure:

```
/
    ...
    foo/
        settings.py
            ...
        models/
            __init__.py
                from .qux import Qux
            qux.py
                ...
```

After merging in the blueprint for model "bar" from the above example, the structure would be:

```
/
    ...
    foo/
        settings.py
            ...
        models/
            __init__.py
                from .qux import Qux
                from .bar import Bar
            bar.py
                from django.db import models
                class Bar(models.Model):
                    pass
            qux.py
                ...
```

# Implementation Details

Django CLI is written in Python and depends on:

## Command Parsing

Django CLI uses `click` to handle CLI input. 

## Rendering

Django CLI uses `Jinja2` to render templates.

## Registry & Virtual environment

In order to support blueprint generation, Django CLI builds a registry of CLI-compatible addons that contain blueprints.
To do this, it has to install all of the current application's dependencies. This is done in a virtual environment created using Python 3's venv API.

Once the application and its dependencies are installed, Django CLI looks through each of the `INSTALLED_APPS` packages for
a `blueprints` subdirectory that contains subpackages matching a blueprint's signature: `generate.py` and `templates`.
