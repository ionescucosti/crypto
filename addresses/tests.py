import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet.settings")
django.setup()

from rest_framework import status
from rest_framework.test import APITestCase
from addresses.models import Addresses


class AddressesTestCases(APITestCase):
    def test_generate_valid_address(self):
        currencies = ['btc', 'eth', 'dot']
        for c in currencies:
            response = self.client.post(f'http://127.0.0.1:8000/generate/{c}/')
            address = json.loads(response._container[0])['address']
            last_address = Addresses.objects.all().order_by('-id')[0]

            self.assertEqual(last_address.address, address)
            self.assertEqual(c, last_address.currency)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_generate_wrong_address(self):
        response = self.client.post(f'http://127.0.0.1:8000/generate/xrp/')
        message = json.loads(response._container[0])['message']
        print(message)
        self.assertEqual('Only BTC, ETH or DOT are supported.', message)

    def test_get_list(self):
        response = self.client.get('http://127.0.0.1:8000/list/')
        addresses_list = Addresses.objects.all()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(addresses_list), len(response.data))

    def test_get_address(self):
        response = self.client.get('http://127.0.0.1:8000/address/1/')
        expected_result = Addresses.objects.all().order_by('id')[0]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
        self.assertEqual(expected_result.id, response.json()['id'])
        self.assertEqual(expected_result.address, response.json()['address'])
        self.assertEqual(expected_result.currency, response.json()['currency'])
