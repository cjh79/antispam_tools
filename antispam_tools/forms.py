from akismet import SpamStatus
from antispam import akismet
from antispam.captcha.forms import ReCAPTCHA
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured


ANTI_SPAM_LEVEL_NONE = 0
ANTI_SPAM_LEVEL_LOW = 1
ANTI_SPAM_LEVEL_HIGH = 2


class ReCaptchaForm(forms.Form):
    """
    Adds a reCaptcha field to the form. But it is only displayed if creating a new object. If the form is used as an
    edit form, do not use the captcha.
    """
    captcha = ReCAPTCHA(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pop the captcha, we'll re-add it below if necessary. That way it shows up at the bottom of the form (fields
        # is an OrderedDict)
        captcha = self.fields.pop('captcha')

        request = self.request if hasattr(self, 'request') else None

        trusted_user = request and (not request.user.is_anonymous) and (
                request.user.is_staff or is_trusted(request.user))

        instance = self.instance if hasattr(self, 'instance') else None

        if not (instance and instance.id) and not settings.RECAPTCHA_TEST_MODE and not trusted_user:
            # Only include captcha if it's a new signup.
            self.fields['captcha'] = captcha


def is_trusted(user):
    return hasattr(user, 'int') and hasattr(user.int, 'is_trusted') and user.int.is_trusted \
        or hasattr(user, 'is_trusted') and user.is_trusted


def is_spam(request, content, spam_level=ANTI_SPAM_LEVEL_HIGH):
    ak_request = akismet.Request.from_django_request(request)
    ak_comment = akismet.Comment(content, type='comment', )
    # ak_author = akismet.Author(name=self.cleaned_data['name'], email=self.cleaned_data['email'])

    if spam_level == ANTI_SPAM_LEVEL_HIGH:
        bad_results = (SpamStatus.ProbableSpam, SpamStatus.DefiniteSpam,)
    elif spam_level == ANTI_SPAM_LEVEL_LOW:
        bad_results = (SpamStatus.DefiniteSpam,)
    else:
        bad_results = ()

    if request and len(bad_results):
        if akismet.check(request=ak_request, comment=ak_comment) in bad_results:
            return True

    return False


class AntiSpamForm(forms.Form):
    """
    Checks content for spam using Akismet service.

    Set the "request" property on an instance in order to allow trusted users to bypass the check.
    """

    def __init__(self, *args, **kwargs):
        # Default setting is appropriate for a Slugged RichText instance which is a typical case.
        self.spam_content_fields = ['content', 'title']
        super().__init__(*args, **kwargs)

    def clean(self):
        request = self.request if hasattr(self, 'request') else None
        disabled_via_settings = getattr(settings, 'AKISMET_TEST_MODE', False) or getattr(settings, 'ANTI_SPAM_LEVEL', None) == ANTI_SPAM_LEVEL_NONE
        has_user = request is not None and (not self.request.user.is_anonymous)
        trusted_user = has_user and (request.user.is_staff or is_trusted(request.user))

        if not (disabled_via_settings or trusted_user):
            spam_content = ' '.join([self.cleaned_data[field] for field in self.spam_content_fields])
            if is_spam(request, spam_content):
                request.user.is_active = False
                request.user.save()
                self.report_spam(spam_content)
                raise ValidationError('Spam detected', code='spam-protection')
        return super().clean()

    def report_spam(self, spam_content):
        """
        Hook for subclasses to override to provide spam reporting as needed.
        :param spam_content:
        :return:
        """
        pass

    def is_spam(self, spam_content):
        return is_spam(self.request if self.request else None, spam_content, spam_level=self.get_spam_level())

    def get_spam_level(self):
        """
        Subclasses should override this if they have their own mechanism for determining spam level, such as mezzanine's
        editable settings object.
        :return:
        """
        return getattr(settings, 'ANTI_SPAM_LEVEL', ANTI_SPAM_LEVEL_HIGH)

