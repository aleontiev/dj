dj: the Django CLI
==================

   * [Getting Started](#getting-started)
      * [Installation](#installation)
      * [Commands](#commands)
         * [info](#info)
         * [init](#init)
         * [add](#add)
         * [remove](#remove)
         * [generate](#generate)
         * [run](#run)
         * [lint](#lint)
         * [test](#test)
   * [Developer's Guide](#developers-guide)
      * [Principles](#principles)
         * [Consistency](#consistency)
         * [Clarity](#clarity)
      * [Blueprints](#blueprints)
         * [Context](#context)
         * [Templates](#templates)
            * [Rendering](#rendering)
            * [Merging](#merging)

   * [Dependencies](#dependencies)
      * [redbaron](#redbaron)
      * [click](#click)
      * [jinja2](#jinja2)
      * [virtualenv](#virtualenv)
      * [pyenv](#pyenv)

# Getting Started

`dj` is a command-line tool that automates Django application developer workflows:

* Setting up a new project
* Managing project dependencies
* Building and running the project
* Generating new code stubs

The Python distribution ecosystem often provides an uncertain and segmented experience, especially for newcomers. There are too many options, they don't integrate well, and they don't provide complete functionality.

For example, the typical development environment might use `pyenv` to control the Python runtime version, `virtualenv` to isolate the project's dependencies, `pip` and `setuptools` to specify dependencies, `django-admin` to initialize a project, `manage.py` within the virtual environment to run commands, and a `Makefile` or `run.py` to wrap all of these tools, filling in the gaps between them.

`dj`, inspired by ember-cli, attempts to instead provide a simple, comprehensive, and extendable
interface for the Django development lifecycle.

With `dj`, you can create a new Django app, add a model, and create an instance of that model in *under 60 seconds*:

<a href="https://asciinema.org/a/ak0470s3ofigxdzoy6eatxek8" target="_blank"><img src="https://asciinema.org/a/ak0470s3ofigxdzoy6eatxek8.png" /></a>

## Installation

To install `dj`, simply run [the appropriate installer](./INSTALLERS.md) for your operating system.
`dj` distributes with PyInstaller and runs within an isolated Python environment.

## Commands

Run `dj --help` to see a list of supported commands.
Run `dj SUBCOMMAND --help` for help on any specific subcommand.

### add

Add a dependency to the project. The dependency must be provided in `pip` dependency notation.

If `--dev` is passed, the addon will only be required for testing and local development.
Otherwise, the addon will be installed in production.

If the `addon` has an `init` blueprint, the `init` blueprint will be generated.

For example:

    dj add dynamic-rest==1.5.0
    dj add dynamic-rest --dev
    dj add git+https://github.com/AltSchool/dynamic-rest@master#egg=dynamic-rest

### generate

Generates a set of modules given a blueprint. The blueprint can be prefixed by the name
of an addon and may take several arguments.

The following core blueprints are supported:

#### init
    
The app blueprint, create the application from scratch.

#### model

Create a custom data model and associated test.

#### command
        
Create a custom server command and associated test.

### info

Display information about the current app.

### init

Sets up a shell Django project in the current directory. This command will prompt for all optional arguments, unless passed in.

### lint

Lints code files using `flake8` / fixes with `autopep8`.

### remove

Removes an installed addon, the inverse of `dj add`.

### run

Run any Django command in development mode.

The app is built and run in a virtual environment.
The runtime specified during initialization is used.

### test

Run tests within the project.
This uses `manage.py test` or provided runner (e.g. `py.test`) to run all test cases in the `tests` package.

# Developer's Guide

It is easy to turn an existing Python or Django library into a `dj`-compatible app that be used standalone or
as an addon to another app. The term "addon" is used to mean that the application code can be used as a library
and that its blueprints can be generated.

## Principles

Django apps using `dj` should follow these principles.
Most are recommended, some are required.

### Consistency

Apps should follow a predictable style and structure.

####  An app MUST have a name.

This name should contain only lower-case letters and underscores.

#### An app MUST have only one top-level code package sharing the app's name.

The package name should be the same as the app name.

For example:        

    app "foo" would package all of its code under the "foo" package.

#### An app MUST have a top-level `setup.py` file.
    
The setup.py file is used by Python installer tools (pip, setuptools)
to determine your package's core dependencies and basic information.

This setup.py file should include a `name` for your app, which should match
the name of your primary app package.

This file is generated by `dj init` and is required by most `dj` commands.

#### An app may have a top-level `manage.py` script.

This manage.py script is the Django entrypoint and should be made executable by
entry in the `scripts` directive in `setup.py`.

Django-specific commands like `migrate`, `shell`, and `serve` will not work without this script.
However, generic Python commands `generate`, `test`, and `run` can still be used.

This file is generated automatically by `dj init`.

#### An app may include a top-level `requirements.txt` dependency file.
    
The most common way for apps to install their dependencies is using a pip-formatted requirements file.
When pip installs from a requirements file, it first downloads each required package. It then installs
each package with `python setup.py install`, which can download and install further packages as defined
in the`install_requires` setup directive.
    
The caveat to `requirements.txt` is that pip does not run itself recursively on this file, so library apps
that want to distribute with other dependencies need to add the `setup.py` directives: `install_requires` and 
`dependency_links`.

`dj` works around this by using a special loader in `setup.py` that reduces `requirements.txt`
to `install_requires` and `dependency_links`. This allows you to keep your core dependencies in one place while support both `pip` and `setuptools` installation.

This file is generated automatically by `dj init` and updated by `dj add` and `dj remove`.

#### An app may have a top-level `requirements.txt.dev` dependency file.

This file is used to install development packages that would not be installed in production.

It is generated automatically by `dj init` and updated by `dj add --dev` and `dj remove --dev`.

#### The code package of the app should contain settings.py, wsgi.py, and urls.py packages.
    
These packages are necessary for Django applications to load. A models.py file is recommended.
    
    settings.py:
        Django configuration file, used to define all core and accessory settings.
        
        Try to use a single configuration file between different environments, with environment secrets
        to differentiate instead.
    
    wsgi.py:
        Exports the WSGI server entrypoint, loaded by a WSGI server to access the Django application.

        Configurable by the WSGI_APPLICATION setting (defaults to $APP.wsgi.application)

    urls.py:
        The URL routing file, should export `urlpatterns`, a list of route matching patterns.

These files are generated automatically by `dj init`.

#### An app should be written in a single code style.

    Style should be enforced by a linter (e.g. `flake8`).
    Naming should be kept consistent between different modules.

#### An app should contain a tests package for all unit and integration tests.
    
    The package `foo.models.bar` should be tested by `tests.unit.foo.models.test_bar`.

### Clarity

App code and structure should be easy to understand.

#### An app should only export one package.
    
When dependencies are installed in the pip/setuptools model,
the top-level packages of a dependency are added to the application's environment.

The flexible mapping between dependency and packages can lead to ambiguity, as dependencies can provide conflicting packages.
    
To mitigate this issue, apps should provide a single package that has the same name as the application name.

#### App code should be concise. 

Re-use shared utility code.
Avoid self-repetition in code (DRY).

Use structure to manage frequently growing lists of code components, e.g. models.

For example:
    
    Don't store all of your models in models.py.
    This file will grow to the point where it becomes unweildy.

    Instead, create one file per model, with the complete list
    defined in models/__init__.py for compatability with the Django model loader.

#### App structure should be concise.

Re-use structural patterns.
Avoid creating unnecessary structure.

Create components within your code package.
Components should have a name (the class name).

We can derive a type (the last functional component),
and a prefix (all functional components leading up to the type component).

Use a hierarchical structure to group components together,
either functionally or logically.

For example:
        
    Add models into the `$APP.models` package.
    A model's type is "model", path is "$APP.models", and name is "Foo".

    Add API serializers into the `$APP.api.$VERSION.serializers` package.
    A serializer's type is "serializer", prefix is "$APP.api.v0.serializers", and name is "Foo".

    Add API views into the `$APP.api.$VERSION.views` package.
    A view's type is "view", prefix is "$APP.api.v0", and name is "User".

## Blueprints

Blueprints allows apps that can function as addons to establish structural conventions for
their consumer apps through the code generation features built into `dj`.

A *blueprint* is a Python package with a `context.py` module that describes the input to the generator function
and a `templates` folder that describes the output.

### Context

A blueprint's `context` package should export a single method called `get_context` that serves as a `click`
entrypoint for the blueprint. This entrypoint should describe the required and optional parameters using
`click` decorators and should return the context that will be called by `dj`'s generation methods.

For example:

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

### Templates

A blueprint's templates folder contains `Jinja` template files that are rendered and merged into an existing
application when the blueprint is called. All Jinja files should be suffixed with `.j2`.

#### Rendering

Blueprints are rendered by applying the context passed to `dj`s `generate` method to each of the files
in the `templates` directory. In addition, file names containing double-underscore delimited variables are replaced by values
from the context. The "app" variable is automatically populated by `dj` with the name of the current application.

For example, the model blueprint:
```
/
    {{app}}/
        models/
            __init__.py
                from .{{ name }} import {{ class_name }}
            __name__.py
                from django.db import models
                class {{ class_name }}(models.Model):
                    pass
```

... would be rendered as follows for app "foo" and name "bar":

```
/
    foo/
        models/
            __init__.py
                from .bar import Bar
            bar.py
                from django.db import models
                class Bar(models.Model):
                    pass
```

#### Merging 

After a blueprint has been rendered, it is merged into the current application folder by folder.
The following rules are used for each folder:

* Folders and files in the blueprint that do not already exist within an application are created
* Files within the blueprint that do exist and match exactly are ignored
* Files within the blueprint that do not match are merged using FST analysis (this is done with the awesome [redbaron](https://github.com/PyCQA/redbaron) package.

For example, suppose that app "foo" has the following code and structure:

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

After merging in the blueprint for model "bar" from the above example, the code would look like:

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

# Dependencies

`dj` is written in Python and depends on the following libraries:

## redbaron

`redbaron` is used to merge Python files (FST-merge). This is applied in the `generate` command. `redbaron` comes packaged with `dj`.

## click

`click` provides the CLI framework. All `dj` subcommands are implemented as `click` commands. `click` comes packaged with `dj`.

## jinja2

`Jinja2` is used to render templates by the `generate` command. It comes packaged with `dj`.

## virtualenv

`virtualenv` is used to build the app in an isolated environment. It is used by `dj run` and other executors. The CLI version is used to support multiple runtimes, and it will be installed if not already present.

## pyenv

`pyenv` is used to manage multiple runtimes / versions of Python. `pyenv` will be installed if not already present.
