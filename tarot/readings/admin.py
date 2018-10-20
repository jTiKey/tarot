from django.contrib import admin
from . import models


class ReadingAdmin(admin.ModelAdmin):
    fields = ('question', 'response', 'image', 'email', 'ip_address', 'responded', 'created', )
    readonly_fields = ('created', 'ip_address',)
    list_display = ('email', 'created', 'responded', )


admin.site.register(models.Reading, ReadingAdmin)
