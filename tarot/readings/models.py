from django.core.mail import EmailMessage
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from model_utils.models import TimeStampedModel
from ckeditor.fields import RichTextField

from django.utils.translation import gettext_lazy as _
from django.db import models


class ReadingManager(models.Manager):
    daily_limit = 5

    def today(self):
        return super().get_queryset().filter(created__date=timezone.now().date())

    def done_today(self):
        return self.today().count()

    def daily_limit_reached(self):
        return self.done_today() > self.daily_limit

    def left_today(self):
        return self.daily_limit - self.done_today()

    def user_limit(self, email, ip_address):
        if settings.DEBUG:
            return self.today().filter(email=email).exists()
        else:
            return self.today().filter(Q(email=email,) | Q(ip_address=ip_address)).exists()


class Reading(TimeStampedModel):
    question = models.TextField()
    response = RichTextField(blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    responded = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    objects = models.Manager()
    limits = ReadingManager()

    def __str__(self):
        return f'{self.email} at {self.created}'

    def __init__(self, *args, **kwargs):
        if not self.responded:
            self.old_responded = False
        super().__init__(*args, **kwargs)

    def clean(self):
        # if Reading.limits.daily_limit_reached():
        #     raise ValidationError(_("All spots for today were taken. Try again tomorrow."))

        if Reading.limits.user_limit(email=self.email, ip_address=self.ip_address):
            raise ValidationError(_("You already sent a question today."))
        super(Reading, self).clean()

    def save(self, *args, **kwargs):
        new_reading = False
        if not self.id:
            new_reading = True
        if self.responded and self.responded != self.old_responded:
            send_mail(subject='')

        super().save(*args, **kwargs)

        if new_reading:
            self.send_reading()

    def send_reading(self):
        template = get_template('emails/reading_received.html')
        context = Context({'object': self})
        content = template.render(context)
        msg = EmailMessage("You've got a reading!", content, to=[self.email, ])
        msg.send()

    def send_response(self):
        template = get_template('emails/reading_response.html')
        context = Context({'object': self})
        content = template.render(context)
        msg = EmailMessage("You've got a reading!", content, to=[self.email, ])
        msg.send()
