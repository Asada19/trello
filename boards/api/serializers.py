from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Trello.boards import models
from Trello.boards.models import Board


class BoardSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=256)
    owner = serializers.ForeignKey(User, related_name='Board', on_delete=models.CASCADE)
    background = serializers.ImageField(upload_to='background', blank=True)

    def image_validator(self):
        valid_formats = ['png', 'jpeg', 'jpg']
        if not any([True if self.background.name.endswith(i) else False for i in valid_formats]):
            raise ValidationError(f'{self.background.name} is not a valid image format')

    def create(self, validated_data):
        board = Board(
            title=validated_data['title'],
            background=validated_data['background']
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.background = validated_data.get('background', instance.background)
        instance.save()
        return instance

