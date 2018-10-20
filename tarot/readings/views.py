from django.shortcuts import render
from django.views.generic import CreateView

from tarot.readings import forms
from tarot.readings import models


class IndexView(CreateView):
    model = models.Reading
    form_class = forms.ReadingForm
    template_name = 'index.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queued_readings'] = models.Reading.objects.filter(responded=False).count()
        context['done_readings'] = models.Reading.objects.filter(responded=True).count()
        context['left_readings_today'] = models.Reading.limits.left_today()
        return context


