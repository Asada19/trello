import unittest

from django.contrib.auth import get_user, get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status

from models import Board, Member

User = get_user_model()


def get_image():
    return SimpleUploadedFile(name='test.jpg', content=open('media/background/1273323_aQC75yO.jpg', 'rb').read(),
                              content_type='image/jpeg')


def get_user(pk):
    return User.objects.get(pk=pk)


class MyTestCase(unittest.TestCase):
    def first_test(self):
        self.user1 = User(email='n@user.com', password='foo', first_name='N', last_name='U').save()
        self.user2 = User(email='n2@user.com', password='foo', first_name='N2', last_name='U2').save()
        Board(title='Example', background_img=get_image()).save()
        Member(user=get_user(1), board=Board.objects.get(pk=1)).save()


if __name__ == '__main__':
    unittest.main()


    def test_get_boards(self):
        user = get_user(1)
        self.client.force_login(user)
        response = self.client.get(reverse('board_index'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

