from django import forms

from . import models


class ReadingForm(forms.ModelForm):
    class Meta:
        model = models.Reading
        fields = ['question', 'email', ]
