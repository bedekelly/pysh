import os
import subprocess
from functools import partial

class ShellHandler:
    """Handler for shell commands."""
    def __getattribute__(self, attrname):
        """Override attribute access for dynamic lookup."""#
        if attrname != "cd":
            return partial(subprocess_call, [attrname])
        else:
            return os.chdir

def subprocess_call(command, *moreargs, **kwargs):
    """Allow for partial function to freeze one arg."""
    try:
        command.extend(moreargs)
        subprocess.check_call(command, **kwargs)
    except FileNotFoundError:
        print("pysh: {}: command not found".format(
            command[0]
        ))
    except:
        pass  # Will show up, at least in bash.

sh = ShellHandler()
