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
import os.path
import subprocess
from itertools import chain
from functools import partial as _partial

class _ShellHandler:
    """Handler for shell commands."""
    def __init__(self):
        self.cd = _my_chdir
        self.aliases = {}

    def alias(self, **kwargs):
        self.aliases.update(kwargs)
        print("pysh: {}: alias added".format(
            list(kwargs.keys())[0]))

    def remalias(self, aliasname):
        try:
            del self.aliases[aliasname]
        except KeyError:
            print("pysh: {}: alias not found".format(aliasname))
        else:
            print("pysh: {}: alias removed".format(aliasname))

    def showalias(self, aliasname):
        try:
            print("pysh: {a} is aliased to {d}"
                  "".format(a=aliasname, d=self.aliases[aliasname]))
        except KeyError:
            print("pysh: {}: no such alias".format(aliasname))

    def listalias(self):
        for key in self.aliases.keys():
            self.showalias(key)

    def __getattribute__(self, attrname):
        """Override attribute access for dynamic lookup."""
        if attrname not in object.__getattribute__(self, "aliases"):
            if attrname not in ["cd", "alias", "aliases", "remalias",
                                "showalias", "listalias"]:
                return _my_partial(_subprocess_call, [attrname])
            else:
                return object.__getattribute__(self, attrname)
        else:
            return _my_partial(_subprocess_call,
                               self.aliases[attrname].split())

class _my_partial(_partial):
    def __repr__(self):
        return "pysh call: {} {}".format(self.args[0][0],
                                         self.args[1:] if self.args[1:]
                                            else "")

def _my_chdir(dirpath="~"):
    dirpath = dirpath.replace("~", os.path.expanduser("~"))
    os.chdir(dirpath)

def _subprocess_call(command, *moreargs):
    """Allow for partial function to freeze one arg.
       Can take any comma-separated args, or a list of args, or a
       string of space-separated args (or any combination of them)."""
    def splitify(mylist):
        return [i.split() if type(i)==str else i for i in mylist]
    def flatten(mylist):
        return chain(*mylist)
    if moreargs:
        moreargs = flatten(splitify(moreargs))
        command.extend(moreargs)
    full_command = ' '.join(command)
    full_command = full_command.split(";")
    for command in full_command:
        command = command.split()
        try:
            subprocess.check_call(command)
        except FileNotFoundError:
            print("pysh: {}: command not found".format(
                command[0]
            ))
        except:
            # Any program which fails will print its own error message.
            pass


sh = _ShellHandler()
