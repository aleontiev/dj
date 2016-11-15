==========
Django CLI
==========

-------------------------------------------------------------------------------
django init <APP>
-------------------------------------------------------------------------------

Sets up a shell Django project in the current directory.

-------------------------------------------------------------------------------
django install <ADDON>[@VERSION] [--tests]
-------------------------------------------------------------------------------

Imports a Django CLI addon or PyPi package into the current project.

If --tests is passed, the addon will only be used for testing.

- Updates `requirements.txt` (for test-only dependencies) 
  or `install_requires.txt`/`dependency_links.txt` (for core dependencies)
- If this is a CLI addon, runs the addon's initializer

-------------------------------------------------------------------------------
django generate [ADDON.]<BLUEPRINT> [...ARGS]
-------------------------------------------------------------------------------

Generates a module given a blueprint. The blueprint can be prefixed by the name
of an addon and may take several arguments.

The following core blueprints are supported:

* model

-------------------------------------------------------------------------------
django run <COMMAND> [...ARGS]
-------------------------------------------------------------------------------

Run any Django command in development mode, using a local virtualenv.
