import factory

from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    # Any tests that result in an email being sent should mock the send_mail_template_async function to prevent sending
    # any actual emails. But, just in case, set them all to chris.
    email = factory.Sequence(lambda n: f'chrishawes+unit_test_email_{n}@gmail.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')
