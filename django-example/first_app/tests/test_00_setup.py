from django.test import TestCase

from first_app.models import Setting

class NoSetupTest(TestCase):

    def test_0(self):
        assert Setting.objects.count() == 0
        Setting.objects.create(key='foo', value='bar')
        assert Setting.objects.count() == 1

    def test_1(self):
        assert Setting.objects.count() == 0
        Setting.objects.create(key='foo', value='bar')
        assert Setting.objects.count() == 1


class SetupTest(TestCase):

    def setUp(self):
        Setting.objects.create(key='foo', value='bar')

    def test_0(self):
        assert Setting.objects.count() == 1
        Setting.objects.create(key='foo', value='bar')
        assert Setting.objects.count() == 2

    def test_1(self):
        assert Setting.objects.count() == 1
        Setting.objects.create(key='foo', value='bar')
        assert Setting.objects.count() == 2

