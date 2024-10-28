from django.contrib import admin
from events.models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event)