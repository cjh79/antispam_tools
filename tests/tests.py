from forms import AntiSpamForm, ReCaptchaForm, ANTI_SPAM_LEVEL_NONE, is_spam, ANTI_SPAM_LEVEL_LOW, ANTI_SPAM_LEVEL_HIGH

import vcr
from django import forms
from django.test import TestCase, RequestFactory
from mezzanine.conf import settings
from mock import patch
import factory


probable_spam = '광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔&mu;광주풀싸롱광주마사지&part;광주안마❉광주밤문화 광주유흥후기:orthodox_cross: 광주휴게텔[OPSS][9][COM]오피쓰}광주오피く광주휴게텔μ광주풀싸롱광주마사지∂광주안마❉광주밤문화'


# Note: To force this to definite spam response, make sure the following header is added to the response in the cassette:
# X-Akismet-Pro-Tip: [discard]
definite_spam = 'buy viagra buy viagra buy viagra buy viagra'

not_spam = 'Hello world, this is a cool comment'


class TestAntiSpamForm(AntiSpamForm):
    content = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spam_content_fields = ['content']


class TestReCaptchaForm(ReCaptchaForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)


class TestAntiSpam(TestCase):
    def setUp(self):
        rf = RequestFactory()
        self.request = rf.get('/hello/world/')

        self.vcr = vcr.VCR(
            cassette_library_dir='cassettes',
            record_mode='new_episodes',
            match_on=['uri', 'method'],
        )

        request_factory = RequestFactory()
        self.request = request_factory.get('/some/path/doesnt/matter')

    @vcr.use_cassette(record_mode='new_episodes')
    def test_setting_none(self):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_NONE

        self.assertFalse(is_spam(self.request, not_spam))
        self.assertFalse(is_spam(self.request, probable_spam))
        self.assertFalse(is_spam(self.request, definite_spam))

    def test_setting_low(self):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_LOW

        with self.vcr.use_cassette('not_spam.yaml'):
            self.assertFalse(is_spam(self.request, not_spam))

        with self.vcr.use_cassette('probable_spam.yaml'):
            self.assertFalse(is_spam(self.request, probable_spam))

        # Could not get django-akismet to register definite spam, even after adding the "# X-Akismet-Pro-Tip: [discard]"
        # header to the cassette. Screw it.
        #
        # with self.vcr.use_cassette('definite_spam.yaml'):
        #     self.assertTrue(is_spam(self.request, definite_spam))

    def test_setting_high(self):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_HIGH

        with self.vcr.use_cassette('not_spam.yaml'):
            self.assertFalse(is_spam(self.request, not_spam))

        with self.vcr.use_cassette('probable_spam.yaml'):
            self.assertTrue(is_spam(self.request, probable_spam))

        # Could not get django-akismet to register definite spam, even after adding the "# X-Akismet-Pro-Tip: [discard]"
        # header to the cassette. Screw it.
        #
        # with self.vcr.use_cassette('definite_spam.yaml'):
        #     self.assertTrue(is_spam(self.request, definite_spam))

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_checks_for_spam_if_anti_spam_setting_is_low(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_LOW

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_trusted = False

        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertTrue(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_checks_for_spam_if_anti_spam_setting_is_high(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_HIGH

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_trusted = False

        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertTrue(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_does_not_check_for_spam_if_anti_spam_setting_is_none(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_NONE

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertFalse(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_does_not_check_for_spam_if_user_is_trusted(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_HIGH

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_trusted = True
        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertFalse(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_does_not_check_for_spam_if_user_is_staff_high(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_HIGH

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_staff = True
        self.request.user.save()
        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertFalse(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_does_not_check_for_spam_if_user_is_trusted_low_high(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_LOW

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_trusted = True
        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertFalse(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_does_not_check_for_spam_if_user_is_staff_low(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_LOW

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_staff = True
        self.request.user.save()
        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertFalse(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_does_not_check_for_spam_if_user_is_trusted_none(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_NONE

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_trusted = True
        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertFalse(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_does_not_check_for_spam_if_user_is_staff_none(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_NONE

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_staff = True
        self.request.user.save()
        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertFalse(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_checks_for_spam_if_user_is_anonymous(self, mock_is_spam):
        from django.contrib.auth.models import AnonymousUser
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_HIGH

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)
        self.request.user = AnonymousUser()
        form.request = self.request

        self.assertTrue(form.is_valid())
        self.assertTrue(mock_is_spam.called)

    @patch('forms.is_spam', side_effect=lambda a, b: False)
    def test_anti_spam_form_checks_for_spam_if_request_not_set(self, mock_is_spam):
        settings.ANTI_SPAM_LEVEL = ANTI_SPAM_LEVEL_HIGH

        data = {
            'content': 'Whats up guys',
        }

        form = TestAntiSpamForm(data=data, initial=data)

        self.assertTrue(form.is_valid())
        self.assertTrue(mock_is_spam.called)

    def test_recaptcha_form_displays_recaptcha_if_request_not_set(self):
        form = TestReCaptchaForm(None, data={}, initial={})

        self.assertIn('captcha', form.fields)

    def test_recaptcha_form_does_not_display_recaptcha_if_trusted_user(self):
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_trusted = True

        form = TestReCaptchaForm(self.request, data={}, initial={})

        self.assertNotIn('captcha', form.fields)

    def test_recaptcha_form_does_not_display_recaptcha_if_staff_user(self):
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_staff = True

        form = TestReCaptchaForm(self.request, data={}, initial={})

        self.assertNotIn('captcha', form.fields)

    def test_recaptcha_form_displays_recaptcha_if_not_trusted_user(self):
        from tests.factories import UserFactory
        self.request.user = UserFactory()
        self.request.user.is_trusted = False

        form = TestReCaptchaForm(self.request, data={}, initial={})

        self.assertIn('captcha', form.fields)

    def test_recaptcha_form_displays_recaptcha_if_anonymous_user(self):
        from django.contrib.auth.models import AnonymousUser
        self.request.user = AnonymousUser()

        form = TestReCaptchaForm(self.request, data={}, initial={})

        self.assertIn('captcha', form.fields)
