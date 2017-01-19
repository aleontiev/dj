from dj.commands.dj import dj

if __name__ == '__main__':
    try:
        command()
    except SystemExit as e:
        if e.code:
            raise
