from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import redirect


class Board(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name='Board', on_delete=models.CASCADE)
    background = models.ImageField(upload_to='media', blank=True)
    favorite = models.BooleanField(default=False)

    def image_validator(self):
        valid_formats = ['png', 'jpeg', 'jpg']
        if not any([True if self.background.name.endswith(i) else False for i in valid_formats]):
            raise ValidationError(f'{self.background.name} is not a valid image format')
        # TODO: Если расширения/размер фотографии большой сжимаем не теряя качество.

    def __str__(self):
        return self.title


class Column(models.Model):
    board = models.ForeignKey(Board, related_name='column', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Card(models.Model):
    column = models.ForeignKey(Column, related_name='cards', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{} - {} - {}'.format(self.column.board.name, self.column.title, self.title)


