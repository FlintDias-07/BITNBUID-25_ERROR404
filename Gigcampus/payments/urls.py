from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path('escrow/<int:escrow_id>/', views.escrow_status, name='escrow_status'),
    path('escrow/release/<int:escrow_id>/', views.release_escrow, name='release_escrow'),
]

{
    "python.analysis.extraPaths": [
        "C:/Users/Admin/AppData/Roaming/Python/Python311/site-packages"
    ]
}