#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 17 December 2012 by Eiríkur Hallgrímsson
# Character geek: The 2nd and 3rd i in my name have diacriticals.
# If there is a file-encoding cookie, Python will accept this. (2.x, too)
# 18 December 2012 EH Added StrictDotDict which doesn't allow new keys.
# 28 March 2013 EH PEP-8 compliance, requested by RackSpace
# 30 October 2015 Unused argument (Pylint) fix from John Anderson, janderson@soltra
# 27 September 2019 DotStore class adds simple persistance via JSON files.
"""Simple Library to hold the DotDict class."""

import os
import json


class DotDict(dict):
    """
    Enable use of Javascript/Coffeescript style object notation for dicts.
    The __missing__ method allows chaining creation of nested DotDicts:
    a = DotDict() ; a.foo.bar = 'content'
    Limitation: Expressing keys as attributes limits keys to valid Python
    identifiers.
    """
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__

    def __setattr__(self, key, value):
        if hasattr(value, 'keys'):
            value = DotDict(value)
        self[key] = value

    def __missing__(self, key):
        self[key] = DotDict()
        return self[key]


class StrictDotDict(DotDict):
    """Strict form (subclass) of DotDict.  Does not allow new keys."""
    def __setattr__(self, key, value):
        if key in self:
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value
        else:
            raise KeyError

    def __missing__(self, *args, **kwargs):
        raise KeyError


class DotStore(DotDict):
    """
    This is a simple backing store for DotDict.
    """

    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__

    def __init__(self, filepath):
        "Establish backing store."
        if os.access(filepath, os.R_OK): # We can read it
            self.update(json.load(open(filepath)))
        else:
            open(filepath, 'w').close() # If not writable, just allow exception.
        self.store = filepath

    def __setattr__(self, key, value):
        "When modified, write to the backing file."
        super().__setattr__(key, value) # Dict behavior handled in superclass
        json.dump(self, open(self.store, 'w'), indent=4)
