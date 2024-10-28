from django.urls import path
from . import views


urlpatterns = [
#event views
path('', views.dashboard, name='event_dashboard'),
path('event-search/', views.event_search, name='event_search'),
path('<int:id>/', views.event_details, name='event_details'),

]