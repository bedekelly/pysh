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
        self.cd = _my_chdir
        self.aliases = {}

    def alias(self, **kwargs):
        """Bind an alias to a given command."""
        self.aliases.update(kwargs)
        print("pysh: {}: alias added".format(
            list(kwargs.keys())[0]))

    def rmalias(self, aliasname):
        """Remove an alias if present."""
        try:
            del self.aliases[aliasname]
        except KeyError:
            print("pysh: {}: alias not found".format(aliasname))
        else:
            print("pysh: {}: alias removed".format(aliasname))

    def showalias(self, aliasname):
        """Print the command to which a given alias is bound if present."""
        try:
            print("pysh: {a} is aliased to {d}"
                  "".format(a=aliasname, d=self.aliases[aliasname]))
        except KeyError:
            print("pysh: {}: no such alias".format(aliasname))

    def listalias(self):
        """Print a list of currently stored aliases."""
        for key in self.aliases.keys():
            self.showalias(key)

    def __getattribute__(self, attrname):
        """Override attribute access for dynamic lookup."""
        # Is the attribute in the user's list of aliases? If not:
        if attrname not in object.__getattribute__(self, "aliases"):
            try:
                # Is the object a function defined here?
                object.__getattribute__(self, attrname)
            except AttributeError:
                # If not, return a partial subprocess_call with its name.
                return _my_partial(_subprocess_call, [attrname])
            else:
                # If it is defined here, just return it.
                return object.__getattribute__(self, attrname)
        # If it is aliased to something, return the modified partial func.
        else:
            return _my_partial(_subprocess_call,
                               self.aliases[attrname].split())


class _my_partial(_partial):
    """Extends partial function; overriding __repr__ to print something
    useful when an object's name is referenced (but not called) at the
    interpreter."""
    def __repr__(self):
        # e.g. pysh: call this object to run 'ls --color=auto'
        return "pysh: call this object to run '{} {}'".format(
                self.args[0][0], self.args[1:] if self.args[1] else "")


def _my_chdir(dirpath="~"):
    """Wrapper for os.chdir to allow for Bash expansion."""
    os.chdir(os.path.expanduser(dirpath))


def _subprocess_call(command, *moreargs):
    """Allow for partial function to freeze one arg.
       Can take any comma-separated args, or a list of args, or a
       string of space-separated args (or any combination of them)."""
    def splitify(mylist):
        # Type checking ensures we don't call 'split()' on a list.
        return [i.split() if type(i)==str else i for i in mylist]
    def flatten(mylist):
        return chain(*mylist)
    if moreargs:
        moreargs = flatten(splitify(moreargs))
        command.extend(moreargs)
    for command in ' '.join(command).split(";"):
        # Split commands up by semicolon, like Bash does.
        command = command.split()
        try:
            subprocess.check_call(command)
        except FileNotFoundError:
            print("pysh: {}: command not found".format(command[0]))
        except:
            # Any program which fails will print its own error message.
            pass

sh = _ShellHandler()
