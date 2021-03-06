from django.contrib import messages
from django.utils.translation import gettext_lazy as _
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
        context['last_readings'] = models.Reading.objects.exclude(image__exact='').order_by('-created')[:6]
        return context

    def form_valid(self, form):
        form.instance.ip_address = self.get_ip()
        messages.success(self.request, _('Question received! Wait for the email.'))
        return super().form_valid(form)

    def get_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = self.request.META.get('REMOTE_ADDR')
        return ipaddress

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')





