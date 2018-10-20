from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
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

    def clean(self):
        if Reading.limits.daily_limit_reached():
            raise ValidationError(_("All spots for today were taken. Try again tomorrow."))

        if Reading.limits.user_limit(email=self.email, ip_address=self.ip_address):
            raise ValidationError(_("You already sent a question today."))
        super(Reading, self).clean()
