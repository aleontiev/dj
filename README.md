Django CLI
==========

# Overview

Django CLI is a command-line tool that aims to automate the repetitive workflows necessary
to manage Django application code, particularly:

* Setting up a new project 
* Adding dependencies to the project
* Running the project in an isolated environment
* Generating code stubs

# Why Django CLI?

While there are existing tools that address some of these workflows at the language and framework level
(django-admin/cookiecutter/cog for generation, virtualenv/pyenv/Docker/Makefile for isolated execution),
each tool has its own learning curve, and there are few integration points between them.
The reality of this ecosystem is often an uncertain and un-DRY developer experience, especially
for newcomers. 

Django CLI, insipred by Ember CLI, attempts to fill these gaps by providing a comprehensive yet extendable
interface for Django application development.

# Commands

Run `django --help` to see a list of command, and `django <subcommand> --help` for help on any specific ommand:

## django init

Sets up a shell Django project in the current directory.
This command will prompt for all optional arguments, unless passed in.

## django install <ADDON>[@VERSION] [--dev]

Imports a Django CLI addon or PyPi package into the current project.

If --dev is passed, the addon will only be required for testing and local development.
Otherwise, the addon will be treated as a core package dependency.

In the case of a CLI addon, the addon's initializer will be executed.

## django generate [ADDON.]<BLUEPRINT> [...ARGS]

Generates a module given a blueprint. The blueprint can be prefixed by the name
of an addon and may take several arguments.

The following core blueprints are supported:

* model

## django run <COMMAND> [--docker] [...ARGS]

Run any Django command in development mode.

If --docker is passed, uses Docker to run the app (the Docker CLI must be installed).
Otherwise, a temporary virtual environment will be used to build and run the app.

# Addons

It is easy to turn an existing Python or Django library into a Django-CLI addon.
The only distinction is a `blueprints` module within the application package.
This blueprints module should provide all of the addon's blueprints, including an optional
`init` blueprint that is run at installation time.

## Blueprints

Blueprints allows addons to establish structural conventions for
their implementions through the code generation features built into Django-CLI.

A blueprint is a Python package with a `cli.py` module that describes the input
and a `templates` folder that describes the output.

## cli.py

A blueprint's `cli` package should export a single method called `cli` that serves as a `click`
entrypoint for the blueprint. This entrypoint should describe the required and optional parameters using
`click` decorators and should call the `generate` method provided by Django CLI with a
populated context object.

Example:

```
# django_cli.blueprints.model.cli

import click
from django_cli.click import command
fron django_cli.generate import generate

@command()
@click.argument('name')
def cli(ctx, name):
    ctx.name = name
    return generate(__file__, ctx)
```

## templates

A blueprint's templates folder contains `Jinja` template files that are rendered and merged into an existing
application when the blueprint is called.

### rendering

Blueprints are rendered by applying the context passed to Django CLI's `generate` method to each of the files
in the `templates` directory. In addition, file names containing double-underscore delimited variables are replaced by values
from the context. The "app" variable is automatically populated by Django CLI with the name of the current application.

For example, the model blueprint (`django_cli.blueprints.model.templates`):
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
                from .bar import bar
            bar.py
                from django.db improt models
                class bar(models.Model):
                    pass
```

### merging

After a blueprint has been rendered, it is merged into the current application folder by folder.
The following rules are used for each folder:

* Folders and files in the blueprint that do not already exist within an application are created
* Files within the blueprint that do exist and match exactly are ignored
* For files within the blueprint that do not match:
  * If the blueprint file does not contain the `cli: merge` directive, the user will be prompted to replace the file during generation
  * If the blueprint does contain the `cli: merge` directive, the two files will be merged together statement by statement:
    * Import statements that match exactly are only rendered once
    * Assignment statements that match exactly are only rendered once
    * Assignment statements to the same variable with different list/set/dict-type values have their values merged.

For example, suppose that app "foo" has the following structure:

```
/
    ...
    foo/
        settings.py
            ...
        models/
            __init__.py
                from .qux import qux
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
                from .qux import qux
                from .bar import bar
            bar.py
                from django.db import models
                class bar(models.Model):
                    pass
            qux.py
                ...
```

# Implementation

Django CLI is written in Python but does not actually use Django.
It makes use of the `click` library for handling CLI input, `Jinja2` to support templating, and `PyInstaller`
for distribution.

