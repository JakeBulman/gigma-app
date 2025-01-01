from django.urls import path
from . import views


urlpatterns = [
#event views
path('', views.dashboard, name='event_dashboard'),
path('artist-events', views.artist_events, name='artist_events'),
path('organiser-events', views.organiser_events, name='organiser_events'),
path('organiser-events/<int:event_id>', views.organiser_events, name='organiser_event'),
path('organiser-events/new-event', views.new_event, name='new_event'),
path('organiser-events/new-event-created', views.new_event_created, name='new_event_created'),

path('event-search/', views.event_search, name='event_search'),
path('<int:id>/', views.event_details, name='event_details'),

]