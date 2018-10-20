from django.core.exceptions import ValidationError
from django.utils import timezone
from model_utils.models import TimeStampedModel
from ckeditor.fields import RichTextField

from django.utils.translation import gettext_lazy as _
from django.db import models


class ReadingManager(models.Manager):
    daily_limit = 5

    def done_today(self):
        today = timezone.now().date()
        return Reading.objects.filter(created__date=today).count()

    def daily_limit_reached(self):
        return self.done_today() > self.daily_limit

    def left_today(self):
        return self.daily_limit - self.done_today()


class Reading(TimeStampedModel):
    question = models.TextField()
    response = RichTextField(blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    responded = models.BooleanField(default=False)

    objects = models.Manager()
    limits = ReadingManager()

    def __str__(self):
        return f'{self.email} at {self.created}'

    def clean(self):
        if Reading.limits.daily_limit_reached():
            raise ValidationError(_("All spots for today were taken. Try again tomorrow."))
        super(Reading, self).clean()
