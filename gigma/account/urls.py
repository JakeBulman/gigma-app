from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
path('', views.dashboard, name='profile_dashboard'),

#login/logout URLs
path('dashboard/', views.dashboard, name='profile_dashboard'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),

#change password urls
path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
path('register/', views.register, name='register'),
path('edit/', views.edit, name='edit'),

#disciplines
path('edit-disciplines/', views.edit_disciplines, name='edit_disciplines'),
path('delete-profile-disciplines/<int:id>', views.delete_profile_discipline, name='delete_profile_discipline'),
path('raise-priority-profile-disciplines/<int:id>', views.raise_priority_profile_discipline, name='raise_priority_profile_discipline'),
path('lower-priority-profile-disciplines/<int:id>', views.lower_priority_profile_discipline, name='lower_priority_profile_discipline'),

#images
path('edit-profile-images/', views.edit_profile_images, name='edit_profile_images'),
path('delete-profile-images/<int:id>', views.delete_profile_images, name='delete_profile_images'),
path('raise-priority-profile-images/<int:id>', views.raise_priority_profile_images, name='raise_priority_profile_images'),
path('lower-priority-profile-images/<int:id>', views.lower_priority_profile_images, name='lower_priority_profile_images'),


#user views
path('profile-search/', views.profile_search, name='profile_search'),
path('<int:id>/<slug:stage_slug>/', views.profile_details, name='profile_details'),

#other views
path('discipline-list/', views.discipline_list, name='discipline_list'),
]