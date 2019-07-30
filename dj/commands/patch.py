from __future__ import absolute_import
from click.formatting import HelpFormatter
from dj.utils import style


def patch_help_formatting():
    HelpFormatter._write_usage = HelpFormatter.write_usage
    HelpFormatter.write_usage = _write_usage

    HelpFormatter._write_heading = HelpFormatter.write_heading
    HelpFormatter.write_heading = _write_heading

    HelpFormatter._write_dl = HelpFormatter.write_dl
    HelpFormatter.write_dl = _write_dl


def _write_usage(self, prog, args, prefix="Usage: "):
    prog = style.white(prog)
    args = style.green(args)
    prefix = style.blue(prefix)
    return self._write_usage(prog, args, prefix=prefix)


def _write_heading(self, heading):
    return self._write_heading(style.blue(heading))


def _write_dl(self, rows, **kwargs):
    return self._write_dl([(style.green(r[0]), r[1]) for r in rows], **kwargs)
