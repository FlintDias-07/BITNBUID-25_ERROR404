from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('payments/', include('payments.urls')),
    path('chat/', include('chat.urls')),
    path('portfolio/', include('portfolio.urls')),
]