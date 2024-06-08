from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_box, name='view_box'),
    path('<int:subscription_id>/', views.add_to_box, name='add_to_box'),
    path('<remove_from_box/subscription_id/', views.remove_from_box, name='remove_from_box'),
]
