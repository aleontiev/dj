Django CLI
==========

Overview
--------

Django CLI is a command-line tool that aims to automate the repetitive workflows necessary
to manage Django application code, particularly:

* Creating a new project
* Adding dependencies to that project
* Running the project in an isolated environment
* Generating stubs for models, views, and other patterns

While there are existing tools that address some of these workflows
(django-admin/cookiecutter/cog for generation, virtualenv/pyenv/Docker/Makefile for isolated execution),
each tool has its own learning curve and there are no integration points between them.
The end result of this ecosystem is often a frustrating and uncertain developer experience, especially
for newcomers.

Django CLI, insipred by Ember CLI, attempts to fill these gaps by providing a comprehensive yet extendable
interface for Django app code generation.

django init <APP>
-------------------------------------------------------------------------------

Sets up a shell Django project in the current directory.

django install <ADDON>[@VERSION] [--tests]
-------------------------------------------------------------------------------

Imports a Django CLI addon or PyPi package into the current project.

If --tests is passed, the addon will only be used for testing.

- Updates `requirements.txt` (for test-only dependencies) 
  or `install_requires.txt`/`dependency_links.txt` (for core dependencies)
- If this is a CLI addon, runs the addon's initializer

django generate [ADDON.]<BLUEPRINT> [...ARGS]
-------------------------------------------------------------------------------

Generates a module given a blueprint. The blueprint can be prefixed by the name
of an addon and may take several arguments.

The following core blueprints are supported:

* model

django run <COMMAND> [...ARGS]
-------------------------------------------------------------------------------

Run any Django command in development mode, using a local virtualenv.
