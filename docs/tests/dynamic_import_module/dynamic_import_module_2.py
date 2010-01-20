#!/usr/bin/env python

import imp
import sys

def import_module(path,name,unique_name, globals=None, locals=None, fromlist=None):
# Fast path: see if unique_name has already been imported.
    try:
        return sys.modules[unique_name]
    except KeyError:
        pass

    sys.path.append(path)
    fp, pathname, description = imp.find_module(name)
    sys.path.pop(-1)

    try:
        return imp.load_module(unique_name,fp, pathname, description)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()

mod1=import_module("mod1","module","module1")

#mod2=import_module("mod2","module","module2")
#mod2.test()

mod1.test()

