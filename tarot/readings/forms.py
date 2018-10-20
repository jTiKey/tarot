from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Fieldset, Submit, Div
from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class ReadingForm(forms.ModelForm):
    class Meta:
        model = models.Reading
        fields = ['question', 'name', 'email', ]
        labels = {
            'question': _('Question'),
            'name': _('Your name'),
            'email': _('Your email address'),
        }
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'email@gmail.com'}),
            'question': forms.TextInput(attrs={
                'placeholder': _('You can send one question per day if there are places left')
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ReadingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    'question', css_class='col-sm-12 col-md-12'
                ),
                Div(
                    'name', css_class='col-sm-6 col-md-3'
                ),
                Div(
                    'email', css_class='col-sm-6 col-md-3'
                ),
                Div(
                    Submit('submit', 'Send', css_class='btn btn-primary', css_id='submit'),
                    css_class='col-sm-12 col-md-6 wrapper'
                ),
                css_class='row'
            ),
        )
