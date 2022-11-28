from rest_framework import serializers
from ..models import Board, Column, Card


class ChecklistSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    is_done = serializers.BooleanField(default=False)


class MarkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    color = serializers.CharField(default='#000', max_length=7)


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=300)
    created_on = serializers.DateTimeField()


class CardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=300, required=False)
    date_of_end = serializers.DateTimeField(default_timezone=None, required=False)
    comment = serializers.StringRelatedField()
    files = serializers.StringRelatedField()
    mark = serializers.StringRelatedField()

    def create(self, validated_data):
        return CardSerializer(**validated_data).save()


class ColumnSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30, required=False)

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.save()
        return instance

    def create(self, validated_data):
        return ColumnSerializer(**validated_data).save()


class BoardDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=30, required=False)
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
