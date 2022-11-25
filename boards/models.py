from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse


class Board(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name='Board', on_delete=models.CASCADE)
    background = models.ImageField(upload_to='background', blank=True)  # <--- сжатие изображений по двум праметрам: optimize и progressive

    def image_validator(self):
        valid_formats = ['png', 'jpeg', 'jpg']
        if not any([True if self.background.name.endswith(i) else False for i in valid_formats]):
            raise ValidationError(f'{self.background.name} is not a valid image format')

    def __str__(self):
        return self.title


class Column(models.Model):
    board = models.ForeignKey(Board, related_name='column', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Card(models.Model):
    column = models.ForeignKey(Column, related_name='cards', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='mark_card', blank=True)
    file = models.FileField(upload_to='card_files', blank=True)
    date_of_end = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('card_detail', args=[str(self.id)])

    def __str__(self):
        return '{} - {} - {}'.format(self.column.board.title, self.column.title, self.title)


class Comment(models.Model):
    author = models.ForeignKey(Card, related_name='commentaries', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='comment', on_delete=models.CASCADE)
    text = models.TextField(blank=True)


class Checklist(models.Model):
    title = models.CharField(max_length=30)
    card = models.ForeignKey(Card, related_name='check_list', on_delete=models.CASCADE)


class Checkpoint(models.Model):
    task = models.CharField(max_length=30)
    done = models.BooleanField(default=False)
    checklist = models.ForeignKey(Checklist, related_name='checkpoint', on_delete=models.CASCADE)


class Mark(models.Model):

    COLOR_PALETTE = [
        ("#FFFFFF", "white",),
        ("#000000", "black",),
    ]

    color = ColorField(samples=COLOR_PALETTE)
    card = models.ForeignKey(Card, related_name='mark', on_delete=models.CASCADE)


class Archiwe(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.OneToOneField(User, related_name='archiwe', on_delete=models.CASCADE)


class Favorite(models.Model):
    space = models.JSONField()
    owner = models.OneToOneField(User, related_name='favorite', on_delete=models.CASCADE)
