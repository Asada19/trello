import unittest
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient

from boards.models import Board, Member, LastSeen, Column


client = RequestsClient()
factory = APIRequestFactory()
apiclient = APIClient()

User = get_user_model()


def get_image():
    return SimpleUploadedFile(name='test.jpg', content=open('media/background/1273323_aQC75yO.jpg', 'rb').read(),
                              content_type='image/jpeg')


def get_user(pk) -> Optional[User]:
    try:
        return User.objects.get(pk=pk)
    except:
        print("User does not exists")


class BoardTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User(email='first@gmail.com', password='hello', first_name='Asada', last_name='Rain').save()
        Board(title='Test1', background=get_image(), owner=user1).save()
        Member(user=get_user(1), board=Board.objects.get(pk=1)).save()

    def test_get_board(self):
        user = get_user(1)
        self.client.force_login(user)
        response = self.client.get(reverse('boards'), format='formdata')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_board(self):
        user = get_user(1)
        self.client.force_login(user)
        data = {'title': 'Example', 'background_img': get_image()}
        response = self.client.post(reverse('boards'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 2)

    def test_update_board(self):
        user = get_user(1)
        self.client.force_login(user)
        data = {'title': 'Updated title'}
        response = self.client.patch(reverse('board-details', kwargs={'pk': 1}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_board(self):
        user = get_user(1)
        self.client.force_login(user)
        response = self.client.delete(reverse('board-details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ColumnTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User(email='first@gmail.com', password='hello', first_name='Asada', last_name='Rain').save()
        board1 = Board(title='Test1', background=get_image(), owner=user1).save()
        Member(user=get_user(1), board=Board.objects.get(pk=1)).save()
        column1 = Column(title='Column1', board=Board.objects.get(pk=1))

    def test_get_column(self):
        user = get_user(1)
        self.client.force_login(user)
        response = self.client.get(reverse('board-columns', kwargs={'pk': 1}), format='formdata')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_board(self):
        user = get_user(1)
        self.client.force_login(user)
        data = {'title': 'Example column'}
        response = self.client.post(reverse('board-columns', kwargs={'pk': 1}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Column.objects.count(), 1)

    def test_update_column(self):
        user = get_user(1)
        self.client.force_login(user)
        data = {'title': 'Updated title'}
        response = self.client.patch(reverse('column-detail', kwargs={'column_id': 1}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
