from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_project, name='post_project'),
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('accept-bid/<int:bid_id>/', views.accept_bid, name='accept_bid'),
]