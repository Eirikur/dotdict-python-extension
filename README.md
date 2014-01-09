dotdict-python-extension
========================

Extension to the builtin dict object that allows dot-notation access
to the contents of Python dict objects.  This is my own original code,
which is simpler and much more robust than similar efforts that I found
on the web.

The __missing__ method allows chaining creation of nested DotDicts:
a = DotDict() ; a.foo.bar = 'content'

Limitation: Expressing keys as attributes limits keys to valid Python
identifiers.
