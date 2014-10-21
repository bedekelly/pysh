pysh
====

Very tiny dynamic interface for shell scripting with python. Pipes to come soon (maybe)

```
Examples:
    >>> from sh import sh
    >>> sh.cp("file1", "file2")
    >>> sh.mv("file3", "file4", "file5", "directoryA")
    >>> sh.ls("--color=auto")
        ... ls output ...
    >>>
    >>> sh.asdfghjkl()
    pysh: asdfghjkl: command not found
```
