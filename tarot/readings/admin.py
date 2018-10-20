from django.contrib import admin
from . import models


class ReadingAdmin(admin.ModelAdmin):
    fields = ('question', 'name', 'response', 'image', 'email', 'ip_address', 'responded', 'created', )
    readonly_fields = ('created', 'ip_address', 'name',)
    list_display = ('email', 'created', 'responded', )


admin.site.register(models.Reading, ReadingAdmin)
