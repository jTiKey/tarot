from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Fieldset, Submit, Div
from django import forms

from . import models


class ReadingForm(forms.ModelForm):
    class Meta:
        model = models.Reading
        fields = ['question', 'email', ]

    def __init__(self, *args, **kwargs):
        super(ReadingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    'question', css_class='col-sm-12 col-md-12'
                ),
                Div(
                    'email', css_class='col-sm-12 col-md-6'
                ),
                Div(
                    Submit('submit', 'Send', css_class='btn btn-primary', css_id='submit'),
                    css_class='col-sm-12 col-md-6 wrapper'
                ),
                css_class='row'
            ),
        )
