from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

from . import models


class ReadingAdmin(admin.ModelAdmin):
    fields = ('question', 'name', 'response', 'image', 'email', 'ip_address', 'responded', 'created', )
    readonly_fields = ('created', 'ip_address', 'name', 'question', 'email')
    list_display = ('email', 'created', 'responded', )
    list_filter = ('responded', )


admin.site.register(models.Reading, ReadingAdmin)

admin.site.unregister([Group, Site, ])
