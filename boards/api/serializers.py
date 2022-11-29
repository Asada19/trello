from rest_framework import serializers
from ..models import Board, Column, Card, Favorite


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        return FileSerializer(**validated_data).save()


class ChecklistSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    is_done = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return ChecklistSerializer(**validated_data).save()

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.is_done = validated_data["is_done"]
        instance.save()
        return instance


class MarkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    color = serializers.CharField(max_length=7, default='#000')

    def create(self, validated_data):
        return MarkSerializer(**validated_data).save()

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.color = validated_data["color"]
        instance.save()
        return instance



class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=300)
    created_on = serializers.DateTimeField()
    author = serializers.StringRelatedField()


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comment'] = CommentSerializer(instance.comment.all(), many=True, context=self.context).data
        representation['files'] = FileSerializer(instance.files.all(), many=True, context=self.context).data
        representation['mark'] = MarkSerializer(instance.mark.all(), many=True, context=self.context).data
        return representation


class ColumnSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cards'] = CardSerializer(instance.cards.all(), many=True, context=self.context).data
        return representation

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
    is_active = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.background = validated_data["background"]
        instance.is_active = validated_data["is_active"]
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['column'] = ColumnSerializer(instance.column.all(), many=True, context=self.context).data
        return representation


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['column'] = ColumnSerializer(instance.column.all(), many=True, context=self.context).data
        return representation


class FavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    board = serializers.IntegerField()
    owner = serializers.IntegerField()

    def create(self, validated_data):
        return FavoriteSerializer(**validated_data).save()



