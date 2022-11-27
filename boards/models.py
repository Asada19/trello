from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Board(models.Model):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name='Board', on_delete=models.CASCADE)
    background = models.ImageField(upload_to='background', blank=True)

    def image_validator(self):
        valid_formats = ['png', 'jpeg', 'jpg']
        if not any([True if self.background.name.endswith(i) else False for i in valid_formats]):
            raise ValidationError(f'{self.background.name} is not a valid image format')

    def __str__(self):
        return self.title

    def save(self):
        image = Image.open(self.background)
        img_output = BytesIO()
        image.save(img_output, "JPEG", optimize=True, progressive=True, quality=40)  # <--- сжатие изображений по двум праметрам: optimize и progressive
        self.background_img = File(img_output, name=self.background.name)
        super().save()


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
    date_of_end = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('card_detail', args=[str(self.id)])

    def __str__(self):
        return '{} - {} - {}'.format(self.column.board.title, self.column.title, self.title)


class Comment(models.Model):
    card = models.ForeignKey(Card, related_name='comment', on_delete=models.CASCADE)
    text = models.TextField(blank=True, max_length=300)
    created_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Checklist(models.Model):
    title = models.CharField(max_length=30)
    card = models.ForeignKey(Card, related_name='check_list', on_delete=models.CASCADE)


class Checkpoint(models.Model):
    task = models.CharField(max_length=30)
    done = models.BooleanField(default=False)
    checklist = models.ForeignKey(Checklist, related_name='checkpoint', on_delete=models.CASCADE)


class Mark(models.Model):
    card = models.ForeignKey(to=Card, on_delete=models.CASCADE, related_name='mark')
    color = models.CharField(default='#000', max_length=7)


class Archiwe(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.OneToOneField(User, related_name='archiwe', on_delete=models.CASCADE)


class Favorite(models.Model):
    space = models.JSONField()
    owner = models.OneToOneField(User, related_name='favorite', on_delete=models.CASCADE)


class File(models.Model):
    card = models.ForeignKey(to=Card, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='card_files/')

    def __str__(self):
        return self.file