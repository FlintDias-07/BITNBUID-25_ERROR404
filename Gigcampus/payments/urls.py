from django.urls import path
from . import views

urlpatterns = [
    path('escrow/<int:escrow_id>/', views.escrow_status, name='escrow_status'),
    path('release/<int:escrow_id>/', views.release_escrow, name='release_escrow'),
]