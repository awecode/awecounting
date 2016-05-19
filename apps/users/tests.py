from django.test import TestCase

from .models import Company


class FyTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='One Pvt. Ltd', location='aaa', organization_type='non_profit')

    def test_fy_from_date(self):
        print(self.company.fy)
