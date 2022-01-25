import pytest

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@test.com'
        password = 'VerySecureP@55word'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        user = get_user_model().objects.first()
        assert user.email == email
        assert user.check_password(password)

    def test_new_user_email_normalized(self):
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        user = get_user_model().objects.first()
        assert user.email == email.lower()

    def test_new_user_invalid_email(self):
        with pytest.raises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )
        user = get_user_model().objects.first()
        assert user.is_superuser
        assert user.is_staff

