from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
  event_display = ('day', 'start_time', 'end_time','notes')

# Register your models here.
admin.site.register(Event, EventAdmin)
