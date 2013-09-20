import os
import unittest
import mock
import urllib2

from captcha import fields
from django.forms import Form


class TestForm(Form):
    captcha = fields.ReCaptchaField(attrs={'theme': 'white'})


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.urlopen = urllib2.urlopen
        splitlines = mock.Mock()
        splitlines.splitlines = mock.Mock(return_value=['false', 'invalid-request-cookie'])
        read = mock.Mock(return_value=splitlines)
        opener = mock.Mock()
        opener.read = read
        urllib2.urlopen = mock.Mock(return_value=opener)

    @classmethod
    def tearDownClass(cls):
        urllib2.urlopen = cls.urlopen

    def setUp(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def test_envvar_enabled(self):
        form_params = {'recaptcha_response_field': 'PASSED'}
        form = TestForm(form_params)
        self.assertTrue(form.is_valid())

    def test_envvar_disabled(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'
        form_params = {'recaptcha_response_field': 'PASSED'}

        form = TestForm(form_params)
        self.assertFalse(form.is_valid())

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']
