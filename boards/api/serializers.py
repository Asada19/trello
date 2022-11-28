from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import Board, Column, Card


# class CommentSerializer(serializers.Serializer):
#     text = serializers.TextField(blank=True, max_length=300)
#     created_on = serializers.DateTimeField(auto_now_add=True)
#
#
# class CardSerializer(serializers.Serializer):
#     # comment = serializers.StringRelatedField(CommentSerializer)
#
#     column = serializers.StringRelatedField(Column, related_name='cards')
#     title = serializers.CharField(max_length=255)
#     description = serializers.StringRelatedField(blank=True)
#     members = serializers.StringRelatedField(related_name='mark_card', blank=True)
#     date_of_end = serializers.StringRelatedField(auto_now=True)


#
#

class ColumnSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    # card = serializers.StringRelatedField(many=True)

    def create(self, validated_data):
        return ColumnSerializer(**validated_data).save()


class BoardDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=50, required=False)
    background = serializers.ImageField(required=False)
    column = serializers.StringRelatedField(many=True, read_only=True)


class BoardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    background = serializers.ImageField(required=False)

    def create(self, validated_data):
        board = Board(
            title=validated_data['title'],
            background=validated_data['background'],
        )
        board.save()
        return board
