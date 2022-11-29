from django import forms
from django.forms import DateTimeInput, TextInput, inlineformset_factory

from .models import Card, Board, Comment, Mark


class BoardCreationForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'background']


class CardCreationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'


class SearchForm(forms.Form):
    user = forms.CharField(label='Search user', max_length=250)
    mark = forms.CharField(label='Search mark', max_length=250)


class CardUpdateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('title', 'description')
        # widgets = {
        #     'date_of_end': DateTimeInput(attrs={"type": "datetime-local", 'required': 'False'})
        # }


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('color', 'title')
        widgets = {
            'color': TextInput(attrs={"type": "color", })
        }


MarkFormset = inlineformset_factory(
    Card,
    Mark,
    form=MarkForm,
    extra=1,
    can_delete=False,
)
