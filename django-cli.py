from django_cli.commands.django import command

if __name__ == '__main__':
    try:
        command()
    except SystemExit as e:
        if e.code:
            raise
