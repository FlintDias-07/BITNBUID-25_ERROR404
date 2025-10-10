from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('field-demand/', views.field_demand, name='field_demand'),
    path('analytics/', views.analytics, name='analytics'),
    path('projects/', include('projects.urls')),
    path('payments/', include('payments.urls')),
    path('chat/', include('chat.urls')),
    path('portfolio/', include('portfolio.urls')),
]