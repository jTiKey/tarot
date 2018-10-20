from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import get_template, render_to_string
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
    image = models.ImageField(blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    responded = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    objects = models.Manager()
    limits = ReadingManager()

    def __str__(self):
        return f'{self.email} at {self.created}'

    def clean(self):
        # if Reading.limits.daily_limit_reached():
        #     raise ValidationError(_("All spots for today were taken. Try again tomorrow."))

        if not self.id and Reading.limits.user_limit(email=self.email, ip_address=self.ip_address):
            raise ValidationError(_("You already sent a question today."))
        super(Reading, self).clean()

    def save(self, *args, **kwargs):
        new_reading = False
        if not self.id:
            new_reading = True
        if self.response and not self.responded:
            self.send_response()
            self.responded = True

        super().save(*args, **kwargs)

        if new_reading:
            self.send_reading()

    def send_reading(self):
        template = get_template('emails/reading_received.html')
        context = {'object': self}
        subject = "You've got a reading!"
        body = template.render(context)

        email = EmailMultiAlternatives(
            subject,
            body,
            settings.WEBSITE_MAIL,
            ['simonneighten@gmail.com', ]
        )
        email.attach_alternative(body, "text/html")
        # if file_path:
        #     email.attach_file(file_path)
        email.send()

    def send_response(self):
        template = get_template('emails/reading_response.html')
        context = {'object': self}
        subject = "jTiKey Reading Response"
        body = template.render(context)

        email = EmailMultiAlternatives(
            subject,
            body,
            settings.WEBSITE_MAIL,
            [self.email, ]
        )
        email.attach_alternative(body, "text/html")
        # if self.image:
        #     email.attach_file(self.image.path)
        email.send()
