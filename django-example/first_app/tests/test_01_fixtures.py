from django.test import TestCase

from first_app.models import Setting


class FixtureTest(TestCase):
    fixtures = ['data']

    def test_0(self):
        assert Setting.objects.count() == 2
        Setting.objects.first().delete()
        assert Setting.objects.count() == 1

    def test_1(self):
        assert Setting.objects.count() == 2


class MultipleFixturesTest(TestCase):
    fixtures = ['more_data']

    def test_0(self):
        assert Setting.objects.count() == 4
