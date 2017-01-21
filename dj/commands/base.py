from __future__ import absolute_import

from dj.utils.system import StyleStdout
import click

stdout = StyleStdout()

from .patch import patch_help_formatting
patch_help_formatting()


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
                stdout.write(
                    'Did you mean one of: %s' %
                    ', '.join(
                        sorted(matches)))
                return None
            else:
                name = matches[0]

        return self.commands.get(name)
