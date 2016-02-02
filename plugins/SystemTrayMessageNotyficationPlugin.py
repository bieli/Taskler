# -*- coding: utf-8 -*-
#
# Plugin for "taskler" system witch displays notification
# messages in system tray bar.
#
# Self-test usage info:
# Usage plugin like script from command line
#  $ __main__ <title> <message>
#  ---
#  <title>   - title for notification bubble
#  <message> - message for notification bubble
#
# @contact:    bieli@bieli.net
# @author:     Marcin Bielak
# @todo:       clear code, add more comments

try:
    from plugins.PluginProvider import Plugin

    PluginProvider_is_available = True
except ImportError:
    class Plugin:
        pass

    PluginProvider_is_available = False

try:
    import pynotify

    pynotify_is_available = True
except ImportError:
    pynotify_is_available = False


class Notification:
    """This class handles the display of visual notification bubbles."""

    def __init__(self, settings, appname):
        """Initialize the class."""

        self.notifications = []  # This list holds the instances of all notifications

        if pynotify_is_available is not True:
            return None

        self.settings = settings
        pynotify.init(appname)

    def script_usage(self):
        print
        "Usage plugin like script from command line:"
        print
        "$ %s <title> <message>" % (self.__module__)
        print
        "---"
        print
        "<title>   - title for notification bubble"
        print
        "<message> - message for notification bubble"

    def showNotification(self, title, message, urgency=0, expires=15000, category='transfer',
                         image='../data/qttube-32x32.png'):
        """Displays a notification bubble."""

        if pynotify_is_available is not True:
            return 0

        if category == 'transfer.notifyDone' and not self.settings.value('Interface/notifyDone').toBool():
            return 0

        if category == 'transfer.notifyError' and not self.settings.value('Interface/notifyError').toBool():
            return 0

        image = '/'.join(__file__.split('/')[0:-1]) + '/' + image

        bubble = pynotify.Notification(title, message, image)

        bubble.set_category(category)
        bubble.set_hint('desktop-entry', 'qttube')
        # bubble.set_hint('x', '0')
        # bubble.set_hint('y', '0')

        if urgency == 0:
            bubble.set_urgency(pynotify.URGENCY_LOW)
        elif urgency == 2:
            bubble.set_urgency(pynotify.URGENCY_CRITICAL)

        if expires == 0:
            bubble.set_timeout(pynotify.EXPIRES_NEVER)
        else:
            bubble.set_timeout(expires)

        bubble.show()
        self.notifications.append(bubble)

    def getNotifications(self):
        """Returns a list with the instances of all notifications."""

        return self.notifications


class SystemTrayMessageNotyficationPlugin(Plugin):
    capabilities = ['reporter', 'init', 'deinit', 'next_item',
                    'proccess', 'set_data', 'get_data',
                    'get_data_count', 'set_verbose']
    DATA = []
    VERBOSE_PREFIX = "plugin verbose mode >> "
    VERBOSE = False

    def reporter(self):
        return 'Hello %s!' % __name__

    def plugin_init(self):
        if True == self.VERBOSE:
            print
            self.VERBOSE_PREFIX + 'init from "%s"!' % __name__

        return True

    def plugin_deinit(self):
        if True == self.VERBOSE:
            print
            self.VERBOSE_PREFIX + 'deinit from "%s"!' % __name__

        return True

    def plugin_proccess(self):
        if True == self.VERBOSE:
            print
            self.VERBOSE_PREFIX + 'proccess from "%s"!' % __name__

        output_data = self.DATA

        #        print str(self.DATA)

        for message in self.DATA['test_msg']:
            self.show_notification(message['title'], message['message'],
                                   message['app_name'], message['app_sub_name'])

        self.DATA = output_data

        return True

    def plugin_next_item(self):
        if True == self.VERBOSE:
            print
            self.VERBOSE_PREFIX + 'next_item from "%s"!' % __name__

        return True

    def plugin_set_data(self, data):
        if True == self.VERBOSE:
            print
            self.VERBOSE_PREFIX + 'set_data from "%s"!' % __name__

        self.DATA = data
        return True

    def plugin_get_data(self):
        if True == self.VERBOSE:
            print
            self.VERBOSE_PREFIX + 'get_data from "%s"!' % __name__

        return self.DATA

    def plugin_get_data_count(self):
        proccesed_data_length = len(self.DATA)

        if True == self.VERBOSE:
            print
            self.VERBOSE_PREFIX + 'get_data_count from "%s"!' % __name__
            print
            self.VERBOSE_PREFIX + 'proccesed_data_length = "%d"!' % \
                                  proccesed_data_length

        return proccesed_data_length


    def set_verbose(self, verbose):
        self.VERBOSE = verbose
        return True

    def show_notification(self, title, message, app_name='',
                          app_sub_name=''):
        """ show notification in system desktop """

        #TODO: need check if X sever is exists (and display is correct?)
        message = 'message: ' + message
        n = Notification(app_name, app_sub_name)
        n.showNotification(title, message)
        return True

# self test plugin code
if __name__ == "__main__" and PluginProvider_is_available == False:
    import sys

    if pynotify_is_available == False:
        print
        "Please install 'pynotify' module for Python in your system !"
        sys.exit()

    if (len(sys.argv) < 2):
        obj = Notification([], "test")
        obj.script_usage()
        sys.exit()
    else:
        obj = Notification([], "test")
        obj.showNotification(sys.argv[1], sys.argv[2])
