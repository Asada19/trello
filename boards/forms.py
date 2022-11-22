from django import forms
from django.core.exceptions import ValidationError

from .models import Board, Card


class BoardCreationForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ['title', 'background']

    # def image_validator(self):
    #     valid_formats = ['png', 'jpeg', 'jpg']
    #     if not any([True if self.background.name.endswith(i) else False for i in valid_formats]):
    #         raise ValidationError(f'{self.background.name} is not a valid image format')


class CardCreationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title']
