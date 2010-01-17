
import sys
import os

class Plugin(object):
    capabilities = []

    def __repr__(self):
        return '<%s %r>' % (
            self.__class__.__name__,
            self.capabilities
        )

_instances = {}

class PluginProvider(Plugin):

    def init_plugin_system(self, cfg):
        if not cfg['plugin_path'] in sys.path:
            sys.path.insert(0, cfg['plugin_path'])

#        print "plugin_path: '%s' " % cfg['plugin_path']

        loaded_plugins = self.load_plugins(cfg['plugins'])

#        print "loaded plugins: '%s' " % loaded_plugins

    def get_plugins_by_capability(self, capability):
        result = []
        for plugin in Plugin.__subclasses__():
#            print "plugin1: '%s' " % plugin
            if capability in plugin.capabilities:
#                print "capability: '%s' " % capability
                if not plugin in _instances:
                    _instances[plugin] = plugin()
                result.append(_instances[plugin])

        return result

    def load_plugins(self, plugins):
        for plugin in plugins:
            __import__(plugin, None, None, [''])

    def find_plugins(self):
        return Plugin.__subclasses__()
