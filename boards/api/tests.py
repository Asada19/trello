from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient


client = RequestsClient()
factory = APIRequestFactory()
apiclient = APIClient()


class BoardTests(APITestCase):
    def test_create_board(self):
        url = reverse('boards')
        data = {'title': 'Test1', 'background': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




