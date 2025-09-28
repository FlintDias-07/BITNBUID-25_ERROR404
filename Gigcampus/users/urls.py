from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/profile/', views.update_profile, name='update_profile'),
    path('settings/notifications/', views.update_notifications, name='update_notifications'),
    path('settings/preferences/', views.update_platform_preferences, name='update_platform_preferences'),
    path('settings/password/', views.change_password, name='change_password'),
    path('api/preferences/', views.get_user_preferences, name='get_user_preferences'),
    path('about/', views.about_view, name='about'),
]