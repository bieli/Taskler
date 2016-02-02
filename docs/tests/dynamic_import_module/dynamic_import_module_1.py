import imp
import sys

# create a module
modname = 'mypackage.mymod'
if sys.modules.has_key(modname):
    mod = sys.modules[modname]

else:
    # create a module
    mod = imp.new_module(modname)

    # store it in sys.modules
    sys.modules[modname] = mod

    # get the package module
    packagemod = __import__('mypackage, globals(), locals(), ['
    mypackage
    '] )

    # add module there too
    setattr(packagemod, 'mymod', mod)

    # our namespace is the module dictionary
    namespace = mod.__dict__

    # test whether this has been done already
    if not hasattr(mod, 'myClass'):
    # compile and exec dynamic code in the module

        exec
    compile(pythoncode, '', 'exec') in namespace

    # get the extension
    extension = namespace.get('myClass')

    # instanciate the object
    myOb = extension()
