"""
PySh
A tiny, intuitive interface to access shell commands as if they were functions
in Python.

Examples:
    >>> from pysh import sh
    >>> sh.cp("file1", "file2")
    >>> sh.mv("file3", "file4", "file5", "directoryA")
    >>> sh.ls("--color=auto")
        ... ls output ...
    >>>
    >>> sh.asdfghjkl()
    pysh: asdfghjkl: command not found

"""

import os
import subprocess
from itertools import chain
from functools import partial as _partial

class _ShellHandler:
    """Handler for shell commands."""
    def __init__(self):
        self.cd = os.chdir
        self.aliases = {}

    def alias(self, **kwargs):
        self.aliases.update(kwargs)

    def __getattribute__(self, attrname):
        """Override attribute access for dynamic lookup."""
        if attrname not in object.__getattribute__(self, "aliases"):
            if attrname not in ["cd", "alias", "aliases"]:
                return _my_partial(_subprocess_call, [attrname])
            else:
                return object.__getattribute__(self, attrname)
        else:
            return partial(_subprocess_call, self.aliases[attrname].split())

class _my_partial(_partial):
    def __repr__(self):
        return "pysh call: {} {}".format(self.args[0][0], self.args[1:] if self.args[1:] else "")

def _subprocess_call(command, *moreargs, **kwargs):
    """Allow for partial function to freeze one arg."""
    def splitify(mylist):
        return [i.split() for i in mylist]
    def flatten(mylist):
        return chain(*mylist)
    if moreargs:
        moreargs = flatten(splitify(list(moreargs)))
        command.extend(moreargs)
    try:
        subprocess.check_call(command, **kwargs)
    except FileNotFoundError:
        print("pysh: {}: command not found".format(
            command[0]
        ))
    except:
        pass  # Will show up, at least in bash.


sh = _ShellHandler()
