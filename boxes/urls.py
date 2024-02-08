from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_box, name='view_box'),
#     path('add/<int:pk>/', views.add_to_box, name='add_to_box')
    path('<int:subscription_id>/', views.add_to_box, name='add_to_box'),
]
