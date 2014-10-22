pysh
====

Very tiny dynamic interface for shell scripting with python. Pipes to come soon (maybe)

####Examples:
```
>>> from pysh import sh
>>> sh.cp("file1", "file2")
>>> sh.mv("file3", "file4", "file5", "directoryA")
>>> sh.ls("--color=auto")
    ... ls output ...
>>>
>>> sh.asdfghjkl()
pysh: asdfghjkl: command not found
```


#####"But how does it work?"
Simple answer: hax.

More complicated answer:
Overloading the __getattribute__ class method. This gets called whenever an  object's attribute is referenced with the 'dot' syntax (or presumably the getattr function, but I haven't tested this). It's pretty aggressive, so you can get into infinite loops pretty quickly if you don't use its parent class's __getattribute__ method with 'self' passed in as the first parameter. The __getattribute__ method gets passed two arguments: the object instance (by convention named 'self') and the name of the attribute which has been referenced. I take that attribute name and return a partial subprocess.call function (i.e. an object that, when called, has the first parameter 'frozen' as the attribute name I pass in when creating the partial function). It's not really the subprocess.call function itself though, it's a kind of wrapper function that allows you either to pass in multiple values as multiple parameters, e.g.:
`>>> sh.ls("--color=auto", "-a")`
or as a single string, e.g.:
`>>> sh.cp("file1 file2 file3 file4 destfolder")
These can also be mixed for clarity, e.g.:
`sh.cp("-r", "directory1 directory2 directory3", "destfolder")`
The wrapper is mainly implemented with the itertools chain function, which flattens the list of arguments.
