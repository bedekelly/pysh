import os
import subprocess
from itertools import chain

class ShellHandler:
    """Handler for shell commands."""
    def __init__(self):
        self.cd = os.chdir
        self.aliases = {}

    def alias(self, **kwargs):
        self.aliases.update(kwargs)

    def __getattribute__(self, attrname):
        """Override attribute access for dynamic lookup."""
        from functools import partial
        if attrname not in object.__getattribute__(self, "aliases"):
            if attrname not in ["cd", "alias", "aliases"]:
                return partial(_subprocess_call, [attrname])
            else:
                return object.__getattribute__(self, attrname)
        else:
            return partial(_subprocess_call, self.aliases[attrname].split())


def _subprocess_call(command, *moreargs, **kwargs):
    """Allow for partial function to freeze one arg."""
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


def splitify(mylist):
    return [i.split() for i in mylist]


def flatten(mylist):
    return chain(*mylist)
