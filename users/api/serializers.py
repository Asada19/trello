from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationAPISerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, required=True, write_only=True)
    password_confirmation = serializers.CharField(min_length=4, required=True, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Password and password confirmation dont match')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                msg = _('Не удается авторизоваться с введенными данными')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Email и пароль обязательны для ввода.')
            raise serializers.ValidationError(msg, code='authorization')

        """
        if user and user.is_active:
        refresh = self.get_token(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        добавить при условии что будет все импортировано attrs['user'] = user
        """
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
            attrs['user'] = {'user_id': user.id, 'user_email': user.email}
        return attrs
