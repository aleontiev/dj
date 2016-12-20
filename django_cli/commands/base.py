from django_cli.application import get_current_application
import click


class BlueprintLoaderCommand(click.MultiCommand):

    @property
    def application(self):
        if not hasattr(self, '_application'):
            self._application = get_current_application()
        return self._application

    @property
    def blueprints(self):
        if not hasattr(self, '_blueprints'):
            blueprints = self.application.get_blueprints()
            self._blueprints = {
                blueprint.name: blueprint for blueprint in blueprints
            }
        return self._blueprints

    def list_commands(self, context):
        return self.blueprints.keys()

    def get_command(self, context, name):
        return self.blueprints[name].load_context()

    def invoke(self, context):
        args = context.protected_args + context.args
        name = args[0]
        try:
            if name not in self.blueprints:
                context.fail(
                    'Could not find blueprint "%s".' % name
                )
        except Exception as e:
            context.fail(str(e))
        context.params['application'] = self.application
        context.params['blueprint'] = self.blueprints[name]
        return super(BlueprintLoaderCommand, self).invoke(context)


class MultiCommand(click.MultiCommand):

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        # alias-by-prefix support
        all_commands = set(self.list_commands(ctx))
        if name not in all_commands:
            matches = [
                x for x in all_commands if x.startswith(name)
            ]
            if not matches:
                return None
            elif len(matches) > 1:
                print 'Did you mean one of: %s' % ', '.join(sorted(matches))
                return None
            else:
                name = matches[0]

        return self.commands.get(name)
