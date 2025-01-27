from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.forms import widgets

from webapp.models import Tag, Article


def at_least_5(string):
    if len(string) < 5:
        raise ValidationError('Поле не может быть короче 5 символов')


class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=50, required=True, validators=(at_least_5,), label="Название")

    class Meta:
        model = Article
        fields = ('title',  'content', 'tags')
        widgets = {
            'tags': widgets.CheckboxSelectMultiple()
        }

    def clean(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        if title and content and title == content:
            raise ValidationError('Заголовок и контент не могут быть равны')

        return super().clean()
