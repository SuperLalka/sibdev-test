import random

from django.test import TestCase
from rest_framework.test import APIClient

from deals.tests.factories import (
    DealsFactory,
    UsersFactory,
)

from deals.models import Deal


class DealsApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_empty_deals(self):
        response = self.client.get('/deals/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_get_deals(self):
        users = [UsersFactory() for _ in range(10)]
        [DealsFactory(customer=random.choice(users)) for _ in range(50)]
        response = self.client.get('/deals/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_post_file(self):
        file_name = "deals_for_test.csv"

        with open("deals/tests/" + file_name) as fp:
            response = self.client.post(
                '/deals/',
                data=fp.read(),
                content_type='text/csv',
                HTTP_CONTENT_DISPOSITION=f"attachment; filename={file_name}",
                CONTENT_TYPE='text/csv',
            )

        self.assertEqual(response.status_code, 204)
        deals = Deal.objects.exists()
        self.assertEqual(deals, True)
