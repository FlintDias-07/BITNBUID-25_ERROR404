from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.portfolio, name='portfolio'),
    path('review/<int:project_id>/', views.add_review, name='add_review'),
]