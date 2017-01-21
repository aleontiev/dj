Django CLI
==========

Django CLI is a command-line tool that automates the repetitive workflows necessary
to manage Django application code:

* Setting up a new project
* Managing project dependencies
* Building and running the project
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

# Principles

Apps should follow these principles:

1. Consistency
a. Apps should contain a `setup.py` setup file.
b. Apps should contain a `manage.py` script defined in `setup.py`.
c. Apps should contain a `requirements.txt` dependency list file.
d. Apps should contain a `requirements.txt.dev` dependency list file.
e. Apps should contain a single app package with the same name as the app.

    The app name (as it appears in package management) should be the same as the package name provided by the app.

f. Apps' app package should contain `settings`, `models`, `wsgi`, `urls` 
    
    These packages are necessary for Django applications.

g. Apps should use a single code style.

    Style should be enforced by a linter (e.g. `flake8`).

h. Apps should test each package in a corresponding subpackage of `tests.unit`.
    
    The package `foo.models.bar` should be tested by `tests.unit.foo.models.test_bar`.

2. Minimalism
a. Apps should only export one package.
    
    When dependencies are installed in the pip/setuptools model,
    the top-level packages of a dependency are added to the application's environment.

    The free mapping between dependency and packages can be confusing, as dependencies and packages can be
    similar but different (e.g. my-dep and my_dep), and dependencies can provide conflicting packages (e.g. my-dep providing foo and other-dep also providing foo).
    
    To mitigate this issue, apps should provide a single package that has the same name as the application name.

b. App code should be concise. 

    Avoid writing code that replaces existing boilerplate.
    Re-use components.

c. App structure should be concise.

    Avoid creating folder structure 

3. Isolation
a. App modules should make dependencies clear.

# Getting Started

## Installation

To install Django CLI, simply run [the appropriate installer](./INSTALLERS.md) for your operating system.
Django CLI distributes with PyInstaller and runs within an isolated Python environment.

## Commands

Run `django --help` to see a list of supported commands.
Run `django SUBCOMMAND --help` for help on any specific subcommand:

### django init NAME

Sets up a shell Django project in the current directory.
This command will prompt for all optional arguments, unless passed in.

### django adds ADDON[@VERSION]

Adds a Django CLI addon or PyPi package into the current project.

If `--dev` is passed, the addon will only be required for testing and local development.
Otherwise, the addon will be treated as a core package dependency.

If this is a Django CLI, the addon's initializer will be generated.

### django generate [ADDON.]BLUEPRINT [...ARGS]

Generates a module given a blueprint. The blueprint can be prefixed by the name
of an addon and may take several arguments.

The following core blueprints are supported:

* model NAME
* command NAME

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
