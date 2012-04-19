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
from funkload.utils import extract_token

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
        self.get(server_url + "/account/login/",
            description="Get /account/login/")
        user = 'test'
        password = 'test'
        csrftoken = extract_token(self.getBody(),'name=\'csrfmiddlewaretoken\' value=\'','\'')
        print "%s\n"%csrftoken
        self.post(server_url + "/account/login/", params=[
            ['csrfmiddlewaretoken',csrftoken],
            ['username', user],
            ['password', password]],description="login")

        # /tmp/tmpswgrBv_funkload/watch0006.request
        self.get(server_url + "/submit/download",
            description="Get /submit/download")
        # /tmp/tmpswgrBv_funkload/watch0007.request
        self.get(server_url + "/submit/1",
            description="Get /submit/1")
        # /tmp/tmpswgrBv_funkload/watch0008.request
        
        self.get(server_url+"/user/input/battleships.in",
            description="Get battleships.in")
        # /tmp/tmpswgrBv_funkload/watch0009.request
        self.post(server_url + "/submit/1", params=[
            ['sourcecode', Upload("foobaz.in")],
            ['output_file', Upload("foobaz.in")]],
            description="Post /submit/1/")


    def test_navigation(self):
        pass
        # end of test -----------------------------------------------

    

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
