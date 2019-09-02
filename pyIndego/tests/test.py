from unittest import TestCase

#import pyIndego
from pyIndego import *
from config import *

class TestAPI(TestCase):
    def test_is_string(self):
        
        CONST_username = username
        CONST_password = password
        CONST_serial = serial

        IndegoAPI_Instance = IndegoAPI(username=CONST_username, password=CONST_password, serial=CONST_serial)
        #assert IndegoAPI_Instance == 'aaa'
        #assert if (IndegoAPI_Instance._login_session)
        assert (IndegoAPI_Instance._login_session) is not None