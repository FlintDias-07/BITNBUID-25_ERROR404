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
    
    # New Analytics URLs
    path('analytics/', views.analytics_view, name='analytics'),
    path('field-demand/', views.field_demand_view, name='field_demand'),
    path('skills-assessment/', views.skills_assessment_view, name='skills_assessment'),
    path('earnings-tracker/', views.earnings_tracker_view, name='earnings_tracker'),
    path('my-projects/', views.my_projects_view, name='my_projects'),
    path('my-bids/', views.my_bids_view, name='my_bids'),
    path('messages/', views.messages_view, name='messages'),
    path('activity-log/', views.activity_log_view, name='activity_log'),
    path('help/', views.help_view, name='help'),
    path('upgrade/', views.upgrade_view, name='upgrade'),
]