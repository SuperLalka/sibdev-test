import random

from django.test import TestCase
from rest_framework.test import APIClient

from deals.tests.factories import (
    DealsFactory,
    UsersFactory,
)


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
