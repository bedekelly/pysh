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
import shlex
import subprocess
from itertools import chain
from functools import partial as _partial

SUPPORTS_COLORS = True
notify_on_success = False

class colors:
    if SUPPORTS_COLORS:
        GREEN = '\033[32m'
        RED = '\033[31m'
        REVERT = '\033[0m'
        BLUE = '\033[34m'

class _ShellHandler:
    """Handler for shell commands."""
    def __init__(self):
        self.cd = _my_chdir
        self.aliases = {}

    def alias(self, **kwargs):
        """Bind an alias to a given command."""
        self.aliases.update(kwargs)
        # We know there should only be one value in kwargs.keys()
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

    def __getattr__(self, attrname):
        """Override attribute access for dynamic lookup."""
        if attrname in self.aliases:
        # If it is aliased to something, return the modified partial func.
            return _my_partial(_subprocess_call,
                               self.aliases[attrname].split())
        else:
        # If not, return a wrapped subprocess call with the ref'd name
            return _my_partial(_subprocess_call, [attrname])


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


def _subprocess_call(command, *moreargs, notify=False, system_notify=False):
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
    for cmd in ' '.join(command).split(";"):
        # Split commands up by semicolon, like Bash does.
        cmd = shlex.split(cmd)  # Split by whitespace, except in quotes.
        try:
            subprocess.check_call(cmd)
        except FileNotFoundError:
            print("pysh: {}: command not found".format(cmd[0]))
            break
        except:
            # Any program which fails will print its own error message.
            break
    else:
        # Operation was fully successful.
        if notify:
            prefix = "{}[+]{} ".format(colors.GREEN, colors.REVERT)
            msg = "pysh: command(s) complete: "
            complete_cmds = "{}{}{}".format(
                colors.GREEN,
                    '{}, {}'.format(
                        colors.REVERT, colors.GREEN
                    ).join(i.strip() for i in ' '.join(command).split(";")),
                colors.REVERT)
            notify_string = prefix + msg + complete_cmds
            print(notify_string)

        if system_notify: # System notification.
            notify_string = ("Pysh commands complete:\n" + '$ '
                             + '\n$'.join(' '.join(command).split(";")))
            subprocess.call(["notify-send", notify_string, "-a", "Terminal"])

sh = _ShellHandler()

sh.ls("--color=auto;pwd;echo 'hello world!'", notify=True)
