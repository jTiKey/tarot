from django.shortcuts import render
from django.views.generic import CreateView

from tarot.readings import forms
from tarot.readings import models


class IndexView(CreateView):
    model = models.Reading
    form_class = forms.ReadingForm
    template_name = 'index.html'
