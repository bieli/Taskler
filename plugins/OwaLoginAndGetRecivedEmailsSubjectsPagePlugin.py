# -*- coding: utf-8 -*-
#
# Plugin for "taskler" system
# witch fetching unreaded messages from OWA e-mail client.
#
# Self-test usage info:
# Usage plugin like script from command line:
#  $ __main__ <owa_url> <login> <password>
#  ---
#  <owa_url>  - url to OWA main login page
#  <login>    - username for login to OWA
#  <password> - password for login to OWA
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

# output file base pattern
BASENAME = "OwaLoginAndGetRecivedEmailsSubjectsPagePlugin"
# the path and filename that you want to use to save your cookies in
COOKIEFILE = '/tmp/' + BASENAME + '_cookies.lwp'
# HTML plugin output
OWA_CHECKER_OUTPUT = '/tmp/' + BASENAME + '_recived_messages.html'

import os.path
import urllib
import re

from BeautifulSoup import BeautifulSoup


class OwaLoginAndGetRecivedEmailsSubjectsPagePlugin(Plugin):
    capabilities = ['reporter', 'init', 'deinit', 'next_item',
                    'proccess', 'set_data', 'get_data',
                    'get_data_count', 'set_verbose']
    DATA = []
    VERBOSE_PREFIX = "plugin verbose mode >> "
    VERBOSE = False

    def script_usage(self):
        print
        "Usage plugin like script from command line:"
        print
        "$ %s <owa_url> <login> <password>" % (self.__module__)
        print
        "---"
        print
        "<owa_url>  - url to OWA main login page"
        print
        "<login>    - username for login to OWA"
        print
        "<password> - password for login to OWA"

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

        output_data = []
        output_data = self.get_email_contents_data(self.DATA['auth'])

        messages = []
        for subject in output_data:
            data_msg = {'title': 'Taskler Owa Checker Notify',
                        'message': str(subject),
                        'app_name': 'Taskler',
                        'app_sub_name': 'v0.2'}

            messages.append(data_msg)

        self.DATA['test_msg'] = messages

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

    def get_email_contents_data(self, auth):
        if True == self.VERBOSE:
            print
            print
            self.VERBOSE_PREFIX + 'from "%s": %s' \
                                  % (__name__, "[INFO] START")

        cj = None
        ClientCookie = None
        cookielib = None

        try:  # Let's see if cookielib is available
            import cookielib
        except ImportError:
            pass
        else:
            import urllib2

            urlopen = urllib2.urlopen
            cj = cookielib.LWPCookieJar()  # This is a subclass of FileCookieJar that has useful load and save methods
            Request = urllib2.Request

        if not cookielib:  # If importing cookielib fails let's try ClientCookie
            try:
                import ClientCookie
            except ImportError:
                import urllib2

                urlopen = urllib2.urlopen
                Request = urllib2.Request
            else:
                urlopen = ClientCookie.urlopen
                cj = ClientCookie.LWPCookieJar()
                Request = ClientCookie.Request

        ####################################################
        # We've now imported the relevant library - whichever library is being used urlopen is bound to the right function for retrieving URLs
        # Request is bound to the right function for creating Request objects
        # Let's load the cookies, if they exist.

        if cj != None:  # now we have to install our CookieJar so that it is used as the default CookieProcessor in the default opener handler
            if os.path.isfile(COOKIEFILE):
                cj.load(COOKIEFILE)
            if cookielib:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                urllib2.install_opener(opener)
            else:
                opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
                ClientCookie.install_opener(opener)

        # If one of the cookie libraries is available, any call to urlopen will handle cookies using the CookieJar instance we've created
        # (Note that if we are using ClientCookie we haven't explicitly imported urllib2)
        # as an example :

        auth_url_params = "owa/auth/owaauth.dll"

        if auth['owa_url'][0] == "/":
            theurl = auth['owa_url'] + auth_url_params
        else:
            theurl = auth['owa_url'] + "/" + auth_url_params

        theurl = theurl + "?url=" + auth['owa_url'] + "&reason=0"

        if True == self.VERBOSE:
            print
            print
            self.VERBOSE_PREFIX + '"%s" : %s' % (__name__, \
                                                 "[INFO] The owa_url: " + theurl)

        txdata = None  # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode

        txheaders = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1;\
                     en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0.011',
                     'Referer': auth['owa_url']}

        params = {
            'destination': auth['owa_url'],
            'flags': '0',
            'forcedownlevel': '0',
            'trusted': '0',
            'username': auth['login'],
            'password': auth['pass'],
            'isUtf8': '1'
        }

        # some Java script functions linked with submit clkLgn() login button
        #function gbid(s){return document.getElementById(s);}
        #function clkLgn(){if(gbid("rdoPrvt").checked){var oD=new Date();oD.setTime(oD.getTime()+2*7*24*60*60*1000);var sA="acc="+(gbid("chkBsc").checked?1:0);var sL="lgn="+gbid("username").value;document.cookie="logondata="+sA+"&"+sL+"; expires="+oD.toUTCString();}}

        txdata = urllib.urlencode(params)

        try:
            req = Request(theurl, txdata, txheaders)  # create a request object
            handle = urlopen(req)  # and open it to return a handle on the url
        except IOError as e:
            if self.VERBOSE:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' \
                                      % (__name__, '[ERROR] We failed to open "%s".' % theurl)
                if hasattr(e, 'code'):
                    print
                    self.VERBOSE_PREFIX + 'from "%s": %s' \
                                          % (__name__, '[ERROR] We failed with error code - %s.' % e.code)
            pass
        else:
            if True == self.VERBOSE:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' \
                                      % (__name__, '[INFO] Here are the headers of the page :')
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' \
                                      % (__name__, handle.info())
                print
                self.VERBOSE_PREFIX + 'from "%s"' % __name__
        # handle.read() returns the page, handle.geturl() returns the true url of the page fetched (in case urlopen has followed any redirects, which it sometimes does)


        if cj == None:
            if True == self.VERBOSE:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, \
                                                         "[ERROR] We don't have a cookie library available - sorry.")
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, \
                                                         "[ERROR] I can't show you any cookies.")
            pass
        else:
            if True == self.VERBOSE:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, \
                                                         'These are the cookies we have received so far :')
                for index, cookie in enumerate(cj):
                    print
                    self.VERBOSE_PREFIX + 'from "%s": %s - %s' \
                                          % (__name__, index, cookie)
            cj.save(COOKIEFILE)  # save the cookies again

        if True == self.VERBOSE:
            if handle is not None:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, \
                                                         "[INFO] Handle is not None.")
            else:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, \
                                                         "[ERROR] Handle is None. Maybe connection shutdowned ...")

        try:
            page_contents = handle.read()
        except:
            if True == self.VERBOSE:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, \
                                                         "[ERROR] Problem with reading from handle")
            pass
        else:
            if True == self.VERBOSE:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' \
                                      % (__name__, \
                                         "[INFO] Readed contents size: '" + str(len(page_contents)) + "'")

                # uncommnt for save content view
                print
                self.VERBOSE_PREFIX + \
                " and write to temporary file '" + OWA_CHECKER_OUTPUT + "'"
                fh = open(OWA_CHECKER_OUTPUT, "w")
                fh.write(page_contents)
                fh.close()

            # -------------------------------------------
        """
        theurl2 = auth['owa_url']

        txdata2 = None

        txheaders2 = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0.011'}

        params2 = None

        # some Java script functions linked with submit clkLgn() login button
        #function gbid(s){return document.getElementById(s);}
        #function clkLgn(){if(gbid("rdoPrvt").checked){var oD=new Date();oD.setTime(oD.getTime()+2*7*24*60*60*1000);var sA="acc="+(gbid("chkBsc").checked?1:0);var sL="lgn="+gbid("username").value;document.cookie="logondata="+sA+"&"+sL+"; expires="+oD.toUTCString();}}

        txdata2 = urllib.urlencode(params2)

        try:
            req2 = Request(theurl2, txdata2, txheaders2)            # create a request object
            handle2 = urlopen(req2)                               # and open it to return a handle on the url
        except IOError, e:
            if True == self.VERBOSE:
                print self.VERBOSE_PREFIX + 'from "%s": %s'\
                    % (__name__, '[ERROR] We failed to open "%s".' % theurl)
                if hasattr(e, 'code'):
                    print self.VERBOSE_PREFIX + 'from "%s": %s'\
                    % (__name__, '[ERROR] We failed with error code - %s.' % e.code)
            pass
        else:
            if True == self.VERBOSE:
                print self.VERBOSE_PREFIX + 'from "%s": %s'\
                 % (__name__, '[INFO] Here are the headers of the page :')
                print self.VERBOSE_PREFIX + 'from "%s": %s'\
                 % (__name__, handle.info())
                print self.VERBOSE_PREFIX + 'from "%s"' % __name__

        try:
            page_contents2 = handle2.read()
        except:
            if True == self.VERBOSE:
                print self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__,\
                   "[ERROR] Problem with reading from handle")
            pass
        else:
            if True == self.VERBOSE:
                print self.VERBOSE_PREFIX + 'from "%s": %s'\
                % (__name__,\
                "[INFO] Readed contents size: '" + str(len(page_contents2))+ "'")

                # uncommnt for save content view
                print self.VERBOSE_PREFIX + \
                " and write to temporary file '" + OWA_CHECKER_OUTPUT+".GET"+"'"
                fh = open(OWA_CHECKER_OUTPUT + ".GET", "w")
                fh.write(page_contents2)
                fh.close()

        soup = BeautifulSoup(page_contents2)
        """

        #TODO: problem with GET contents with COOKIES
        #        url = opener.open(auth['owa_url'])
        #        page_contents2 = url.read(200000)
        #         print page_contents2

        soup = BeautifulSoup(page_contents)
        #p = soup.findAll('html', '')
        #print self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, soup.html.body.table
        #tds = soup.findAll("table", 'lvw')
        tds = soup.findAll("h1", 'bld')
        count = len(tds)
        #re.compile("", '')
        #print self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, "tds len = " + str(count)
        #print self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, tds[0]

        unreaded_mail_messages_subjects = []
        if 0 < count:
            if True == self.VERBOSE:
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' \
                                      % (__name__, "Found " + str(count) + " subject(s) :")

            for id in xrange(len(tds)):
                #print self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, " %d -> %s" % (id, tds[id])
                re_subject_h1 = re.compile('<h1 class="bld"><a href="#" onclick=".*">(.*)</a></h1>')
                subject = re_subject_h1.search(str(tds[id])).groups()[0]
                unreaded_mail_messages_subjects.append(str(subject).strip())
                #TODO
                #                 show_notification("[EMAIL]", subject)
                if True == self.VERBOSE:
                    print
                    self.VERBOSE_PREFIX + 'from "%s": %s' \
                                          % (__name__, "[EMAIL] %d -> %s" % (id, subject))
        else:
            unreaded_mail_messages_subjects = []
            #TODO
            #                show_notification("[EMAIL]", subject)
            if True == self.VERBOSE:
                subject = "[INFO] There was no EMAILs ..."
                print
                self.VERBOSE_PREFIX + 'from "%s": %s' % (__name__, subject)

        if True == self.VERBOSE:
            print
            self.VERBOSE_PREFIX + 'from "%s"' % __name__
            print
            self.VERBOSE_PREFIX + 'from "%s": %s' \
                                  % (__name__, "[INFO] STOP")

            print
            self.VERBOSE_PREFIX + \
            'from "%s": [INFO] unreaded subjects: %s' \
            % (__name__, str(unreaded_mail_messages_subjects))

        return unreaded_mail_messages_subjects

# self test plugin code
if __name__ == "__main__" and PluginProvider_is_available == False:
    import sys

    if (len(sys.argv) < 3):
        obj = OwaLoginAndGetRecivedEmailsSubjectsPagePlugin()
        obj.script_usage()
        sys.exit()
    else:
        obj = OwaLoginAndGetRecivedEmailsSubjectsPagePlugin()
        obj.set_verbose(True)
        unreaded_messages = obj.get_email_contents_data(
            {'owa_url': sys.argv[1],
             'login': sys.argv[2],
             'pass': sys.argv[3]})

        if len(unreaded_messages) > 0:
            for k, v in xrange(unreaded_messages):
                print
                k, v
        else:
            print
            "No messages or problem witch fetching e-mails !"