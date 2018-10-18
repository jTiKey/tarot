from model_utils.models import TimeStampedModel
from ckeditor.fields import RichTextField

from django.db import models


class Reading(TimeStampedModel):
    question = models.TextField()
    response = RichTextField(blank=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email} at {self.created}'
