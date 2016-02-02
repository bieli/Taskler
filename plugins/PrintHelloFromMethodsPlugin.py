# -*- coding: utf-8 -*-

try:
    from plugins.PluginProvider import Plugin

    PluginProvider_is_available = True
except ImportError:
    class Plugin:
        pass

    PluginProvider_is_available = False


class PrintHelloFromMethodsPlugin(Plugin):
    capabilities = ['reporter', 'init', 'deinit', 'next_item',
                    'proccess', 'set_data', 'get_data',
                    'get_data_count', 'set_verbose']
    DATA = []
    VERBOSE_PREFIX = "plugin verbose mode >> "
    VERBOSE = False

    def script_usage(self):
        print("Usage plugin like script from command line:")
        print("$ %s" % self.__module__)
        print("---")
        print("no need arguments")

    def reporter(self):
        return 'Hello %s!' % __name__

    def plugin_init(self):
        if self.VERBOSE:
            print(self.VERBOSE_PREFIX + 'init from "%s"!' % __name__)
        return True

    def plugin_deinit(self):
        if self.VERBOSE:
            print(self.VERBOSE_PREFIX + 'deinit from "%s"!' % __name__)
        return True

    def plugin_proccess(self):
        if self.VERBOSE:
            print(self.VERBOSE_PREFIX + 'proccess from "%s"!' % __name__)

        output_data = self.DATA
        for data in self.DATA:
            data += 10
        self.DATA = output_data

        return True

    def plugin_next_item(self):
        if self.VERBOSE:
            print(self.VERBOSE_PREFIX + 'next_item from "%s"!' % __name__)
        return True

    def plugin_set_data(self, data):
        if self.VERBOSE:
            print(self.VERBOSE_PREFIX + 'set_data from "%s"!' % __name__)
        self.DATA = data
        return True

    def plugin_get_data(self):
        if self.VERBOSE:
            print(self.VERBOSE_PREFIX + 'get_data from "%s"!' % __name__)
        return self.DATA

    def plugin_get_data_count(self):
        proccesed_data_length = len(self.DATA)

        if self.VERBOSE:
            print(self.VERBOSE_PREFIX + 'get_data_count from "%s"!' % __name__)
            print(self.VERBOSE_PREFIX + 'proccesed_data_length = "%d"!' % proccesed_data_length)
        return proccesed_data_length


    def set_verbose(self, verbose):
        self.VERBOSE = verbose
        return True

# self test plugin code
if __name__ == "__main__" and PluginProvider_is_available == False:
    import sys

    obj = PrintHelloFromMethodsPlugin()
    obj.script_usage()

    print
    "OUTPUT RESULTS:"
    print
    obj.reporter()
    sys.exit()
