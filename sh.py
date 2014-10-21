"""
PySh
A tiny, intuitive interface to access shell commands as if they were functions
in Python.

Examples:
    from sh import sh
    sh.cp("file1", "file2")
    sh.mv("file3", "file4", "file5", "directoryA")
    sh.ls("--color=auto")
"""

# Dummy program so as not to clutter the namespace.
from lib.handler import ShellHandler as _ShellHandler
sh = _ShellHandler()
