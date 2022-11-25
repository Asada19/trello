from django import forms
from .models import Card, Board


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


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Leave a comment'
    }))


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'


class SearchForm(forms.Form):
    user = forms.CharField(label='Search user', max_length=250)
    mark = forms.CharField(label='Search mark', max_length=250)

