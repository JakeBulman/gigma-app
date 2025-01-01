from django import forms
from django.contrib.auth.models import User
from .models import Event


class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_datetime', 'event_location']