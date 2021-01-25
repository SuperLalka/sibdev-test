import random

from django.test import TestCase
from memoize import Memoizer
from rest_framework.test import APIClient

from deals.tests.factories import (
    DealsFactory,
    UsersFactory,
)

from deals.models import Deal


class DealsApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.memoizer = Memoizer()

    def test_get_empty_deals(self):
        self.memoizer.clear()
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

        with open("deals/tests/test_files/" + file_name) as fp:
            response = self.client.post(
                '/deals/',
                data=fp.read(),
                content_type='text/csv',
                HTTP_CONTENT_DISPOSITION=f"attachment; filename={file_name}",
            )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Deal.objects.exists(), True)

    def test_post_empty_file(self):
        file_name = "deals_for_test_empty_file.csv"

        with open("deals/tests/test_files/" + file_name) as fp:
            response = self.client.post(
                '/deals/',
                data=fp.read(),
                content_type='text/csv',
                HTTP_CONTENT_DISPOSITION=f"attachment; filename={file_name}",
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Empty content'})

    def test_post_incorrect_file(self):
        file_name = "deals_for_test_incorrect.csv"

        with open("deals/tests/test_files/" + file_name) as fp:
            response = self.client.post(
                '/deals/',
                data=fp.read(),
                content_type='text/csv',
                HTTP_CONTENT_DISPOSITION=f"attachment; filename={file_name}",
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Error")

    def test_post_only_headers_file(self):
        file_name = "deals_for_test_only_headers.csv"

        with open("deals/tests/test_files/" + file_name) as fp:
            response = self.client.post(
                '/deals/',
                data=fp.read(),
                content_type='text/csv',
                HTTP_CONTENT_DISPOSITION=f"attachment; filename={file_name}",
            )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Deal.objects.exists(), False)

    def test_memoization(self):
        file_name = "deals_for_test.csv"

        with open("deals/tests/test_files/" + file_name) as fp:
            self.client.post(
                '/deals/',
                data=fp.read(),
                content_type='text/csv',
                HTTP_CONTENT_DISPOSITION=f"attachment; filename={file_name}",
            )

        response = self.client.get('/deals/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

        Deal.objects.all().delete()

        response = self.client.get('/deals/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)
