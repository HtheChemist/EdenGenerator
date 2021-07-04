from __future__ import print_function

# std imports
import sys

# local
from blessed import Terminal


def progress_bar():
    """Program entry point."""
    term = Terminal()
    assert term.hpa(1) != u'', (
        'Terminal does not support hpa (Horizontal position absolute)')

    col, offset = 1, 1
    with term.cbreak():
        inp = None
        print("press 'X' to stop.")
        sys.stderr.write(term.move_yx(term.height, 0) + u'[')
        sys.stderr.write(term.move_x(term.width - 1) + u']' + term.move_x(1))
        while inp != 'X':
            if col >= (term.width - 2):
                offset = -1
            elif col <= 1:
                offset = 1
            sys.stderr.write(term.move_x(col))
            if offset == -1:
                sys.stderr.write(u'.')
            else:
                sys.stderr.write(u'=')
            col += offset
            sys.stderr.write(term.move_x(col))
            sys.stderr.write(u'|\b')
            sys.stderr.flush()
            inp = term.inkey(0.04)
    print()