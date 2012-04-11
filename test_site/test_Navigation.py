# -*- coding: iso-8859-15 -*-
"""navigation FunkLoad test

$Id: $
"""

import unittest
from funkload.Lipsum import Lipsum
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data
import hashlib
#from funkload.utils import xmlrpc_get_credential

def user_grade_dir_name(username):
    return hashlib.md5(username).hexdigest()[0:5] + username

lipsum = Lipsum()

class Navigation(FunkLoadTestCase):
    """XXX

    This test use a configuration file Navigation.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        # XXX here you can setup the credential access like this
        # credential_host = self.conf_get('credential', 'host')
        # credential_port = self.conf_getInt('credential', 'port')
        # self.login, self.password = xmlrpc_get_credential(credential_host,
        #                                                   credential_port,
        # XXX replace with a valid group
        #                                                   'members')

    def test_download_upload(self):
        server_url = self.server_url
        # /tmp/tmpswgrBv_funkload/watch0003.request
        self.get(server_url + "/account/register/",
            description="Get /account/register/")
        user = lipsum.getUniqWord()
        password = lipsum.getUniqWord()

        self.post(server_url + "/account/register/", params=[
            ['username', user],
            ['password1', password],
            ['password2', password],
            ['email', user+'@example.com'],
            ['first_name', lipsum.getWord()],
            ['last_name', lipsum.getWord()],
            ['grad', '2011-12-01'],
            ['resume', Upload("")]],
            description="Post /account/register/")
        # /tmp/tmpswgrBv_funkload/watch0006.request
        self.get(server_url + "/submit/download",
            description="Get /submit/download")
        # /tmp/tmpswgrBv_funkload/watch0007.request
        self.get(server_url + "/submit/1",
            description="Get /submit/1")
        # /tmp/tmpswgrBv_funkload/watch0008.request
        
        self.get(server_url + "/user/input/foobaz.in",
            description="Get foobaz.in")
        # /tmp/tmpswgrBv_funkload/watch0009.request
        self.post(server_url + "/submit/", params=[
            ['sourcecode', Upload("foobaz.in")],
            ['output_file', Upload("foobaz.in")]],
            description="Post /submit/")


    def test_navigation(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        # /tmp/tmpy7Ii5Y_funkload/watch0002.request
        self.get(server_url + "/account/register/",
            description="Get /account/register/")
        # /tmp/tmpy7Ii5Y_funkload/watch0003.request
        user = lipsum.getUniqWord()
        password = lipsum.getUniqWord()

        self.post(server_url + "/account/register/", params=[
            ['username', user],
            ['password1', password],
            ['password2', password],
            ['email', user+'@example.com'],
            ['first_name', lipsum.getWord()],
            ['last_name', lipsum.getWord()],
            ['grad', '2011-12-01'],
            ['resume', Upload("")]],
            description="Post /account/register/")
        # /tmp/tmpy7Ii5Y_funkload/watch0005.request
        self.get(server_url + "/submit/download",
            description="Get /submit/download")
        # /tmp/tmpy7Ii5Y_funkload/watch0006.request
        self.get(server_url + "/scoreboard/",
            description="Get /scoreboard/")
        # /tmp/tmpy7Ii5Y_funkload/watch0007.request
        self.get(server_url + "/account/logout/",
            description="Get /account/logout/")

        # end of test -----------------------------------------------

    

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
