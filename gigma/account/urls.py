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
path('edit-disciplines/', views.edit_disciplines, name='edit_disciplines'),

#user views
path('profile-search/', views.profile_search, name='profile_search'),
path('<int:id>/', views.profile_details, name='profile_details'),

#other views
path('discipline-list/', views.discipline_list, name='discipline_list'),
]