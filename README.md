PySh
====

Very tiny dynamic interface for shell scripting with python.

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

####Aliases:
Just like in Bash, you can define aliases for shell calls you make regularly.
```
>>> from pysh import sh
>>> sh.alias(ls='ls --color=auto')
>>> sh.ls()
    ... ls output, colored ...
```

#####"But how does it work?"
Simple answer: **hackz**.

More complicated answer:
Overloading the `__getattribute__` class method. This gets called whenever an  object's attribute is referenced with the syntax `object.attribute` (or the `getattr` function, as it turns out).

It's pretty aggressive, so you can get into infinite loops pretty quickly if you don't use its parent class's `__getattribute__` method with `self` passed in as the first parameter. The `__getattribute__` method gets passed two arguments: the object instance (by convention named `self`) and the name of the attribute which has been referenced. I take that attribute name and return a partial `subprocess.call` function (i.e. an object that, when called, has the first parameter 'frozen' as the attribute name I pass in when creating the partial function).

It's not really the `subprocess.call` function itself though, it's a kind of wrapper function that allows some more flexibility when passing in parameters (see examples above).

The wrapper is mainly implemented with the `itertools.chain` function, which can flatten shallow lists. Some type-checking in a list comp means you can also pass in your list of arguments as an iterable, and it will be flattened accordingly.

####Wishlist:
* Multiple shell calls per function/alias, e.g.
```
sh.alias(up = 'sudo apt-get update;'
                'sudo apt-get upgrade -y;'
                'printf "[+] Update completed successfully"'
                )
```
* Colored (red/green) status indicator for each command run, possibly getting the return value from check_call or parsing error messages.
