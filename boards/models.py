from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Board(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name='Board', on_delete=models.CASCADE, null=True)
    background = models.ImageField(upload_to='background', blank=True, null=True)
    members = models.ManyToManyField(to=User, related_name='boards')
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    def image_validator(self):
        valid_formats = ['png', 'jpeg', 'jpg']
        if not any([True if self.background.name.endswith(i) else False for i in valid_formats]):
            raise ValidationError(f'{self.background.name} is not a valid image format')

    def save(self, *args, **kwargs):
        super(Board, self).save(*args, **kwargs)
        if self.background:
            img = Image.open(self.background.path)
            if img.height > 300 or img.width > 300:
                img.save(self.background.path, quality=20, optimize=True)

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
    date_of_end = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('card_detail', args=[str(self.id)])

    def __str__(self):
        return '{} - {} - {}'.format(self.column.board.title, self.column.title, self.title)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='comment', on_delete=models.CASCADE)
    text = models.TextField(blank=True, max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)


class Checklist(models.Model):
    title = models.CharField(max_length=30)
    card = models.ForeignKey(Card, related_name='check_list', on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)


class Checkpoint(models.Model):
    task = models.CharField(max_length=30)
    done = models.BooleanField(default=False)
    checklist = models.ForeignKey(Checklist, related_name='checkpoint', on_delete=models.CASCADE)


class Mark(models.Model):
    card = models.ForeignKey(to=Card, on_delete=models.CASCADE, related_name='mark')
    color = models.CharField(default='#000', max_length=7)
    title = models.CharField(blank=True, max_length=30)


class Favorite(models.Model):
    owner = models.ForeignKey(User, related_name='favorite', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='favorite', on_delete=models.DO_NOTHING, null=True)


class File(models.Model):
    card = models.ForeignKey(to=Card, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='Files/')

    def __str__(self):
        return self.file


class Member(models.Model):
    user = models.ForeignKey(User, related_name='member', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='boar_member', on_delete=models.CASCADE)



