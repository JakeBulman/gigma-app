from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_organiser = models.ForeignKey(User,related_name='organiser_events',on_delete=models.SET_NULL, null=True)
    event_datetime = models.DateTimeField()
    event_location = models.CharField(max_length=100)
    event_website = models.TextField(null=True, blank=True)
    event_description = models.TextField(null=True, blank=True)
    event_private_description = models.TextField(null=True, blank=True)
    event_picture = models.ImageField(upload_to='event_pictures/', blank=True)

    class Meta:
        ordering = ['event_name']
        indexes = [models.Index(fields=['event_name'])]

    def __str__(self):
        return self.event_name
    
    def get_absolute_url(self):
        return reverse('event_details',args=[self.id])