from django.contrib import admin
from . import models


class ReadingAdmin(admin.ModelAdmin):
    fields = ('question', 'response', 'email', 'responded', 'created', )
    readonly_fields = ('created', )
    list_display = ('email', 'created', 'responded', )


admin.site.register(models.Reading, ReadingAdmin)
