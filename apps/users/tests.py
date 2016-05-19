from importlib import import_module

from django.conf import settings
from django.test import TestCase

from .models import Company


class SessionTestCase(TestCase):
    def setUp(self):
        # http://code.djangoproject.com/ticket/10899
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key


class FyTest(SessionTestCase):
    def setUp(self):
        super(FyTest, self).setUp()
        self.company = Company.objects.create(name='One Pvt. Ltd', location='aaa', organization_type='non_profit')

    def test_fy_property(self):
        print(self.company.fy)

    def test_nepali_bs(self):
        self.company.use_nepali_fy_system = True
        self.assertEquals(self.company.get_fy_from_date('2071-09-15'), 2071)
        self.assertEquals(self.company.get_fy_from_date('2072-03-30'), 2071)
        self.assertEquals(self.company.get_fy_from_date('2072-04-01'), 2072)
        self.assertEquals(self.company.get_fy_from_date('2072-09-10'), 2072)
        self.assertEquals(self.company.get_fy_from_date('2073-03-30'), 2072)

    def test_other_ad(self):
        self.company.use_nepali_fy_system = False
        self.assertEquals(self.company.get_fy_from_date('2015-09-15'), 2015)
        self.company.fy_start_month, self.company.fy_start_day = 8, 10
        self.assertEquals(self.company.get_fy_from_date('2014-09-15'), 2014)
        self.assertEquals(self.company.get_fy_from_date('2015-08-09'), 2014)
        self.assertEquals(self.company.get_fy_from_date('2015-08-10'), 2015)
        self.assertEquals(self.company.get_fy_from_date('2015-08-18'), 2015)
        self.assertEquals(self.company.get_fy_from_date('2016-07-18'), 2015)

    def test_start_bs(self):
        self.company.use_nepali_fy_system = True
        self.assertEquals(self.company.get_fy_start('2071-08-12'), (2071, 4, 1))
        self.assertEquals(self.company.get_fy_start('2072-04-1'), (2072, 4, 1))
        self.assertEquals(self.company.get_fy_start('2072-09-15'), (2072, 4, 1))

    def test_end_bs(self):
        self.company.use_nepali_fy_system = True
        self.assertEquals(self.company.get_fy_end('2071-08-12'), (2072, 3, 31))
        self.assertEquals(self.company.get_fy_end('2072-04-1'), (2073, 3, 31))
        self.assertEquals(self.company.get_fy_end('2072-09-15'), (2073, 3, 31))
        self.assertEquals(self.company.get_fy_start('2073-02-01'), (2072, 4, 1))

    def test_start_ad(self):
        self.company.use_nepali_fy_system = False
        self.assertEquals(self.company.get_fy_start('2015-09-15'), (2015, 1, 1))
        self.company.fy_start_month, self.company.fy_start_day = 8, 10
        self.assertEquals(self.company.get_fy_start('2014-09-15'), (2014, 8, 10))
        self.assertEquals(self.company.get_fy_start('2015-08-09'), (2014, 8, 10))
        self.assertEquals(self.company.get_fy_start('2015-08-10'), (2015, 8, 10))
        self.assertEquals(self.company.get_fy_start('2015-08-18'), (2015, 8, 10))
        self.assertEquals(self.company.get_fy_start('2016-07-18'), (2015, 8, 10))

    def test_end_ad(self):
        self.company.use_nepali_fy_system = False
        self.assertEquals(self.company.get_fy_end('2015-09-15'), (2015, 12, 31))
        self.company.fy_start_month, self.company.fy_start_day = 8, 10
        self.assertEquals(self.company.get_fy_end('2014-09-15'), (2015, 8, 9))
        self.assertEquals(self.company.get_fy_end('2015-08-09'), (2015, 8, 9))
        self.assertEquals(self.company.get_fy_end('2015-08-10'), (2016, 8, 9))
        self.assertEquals(self.company.get_fy_end('2015-08-18'), (2016, 8, 9))
        self.assertEquals(self.company.get_fy_end('2016-07-18'), (2016, 8, 9))
