from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient


client = RequestsClient()
factory = APIRequestFactory()
apiclient = APIClient()

User = get_user_model()


def get_image():
    return SimpleUploadedFile(name='test.jpg', content=open('media/background/1273323_aQC75yO.jpg', 'rb').read(),
                              content_type='image/jpeg')


def get_user(pk):
    return User.objects.get(pk=pk)


class BoardTests(APITestCase):
    def test_create_board(self):
        url = reverse('boards')
        data = {'title': 'Test1', 'background': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_boards(self):
        user = get_user(1)
        self.client.force_login(user)
        response = self.client.get(reverse('board_index'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

