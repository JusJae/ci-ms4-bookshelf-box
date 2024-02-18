from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_box, name='view_box'),
#     path('add/<int:pk>/', views.add_to_box, name='add_to_box')
    path('<int:subscription_id>/', views.add_to_box, name='add_to_box'),
    # path('<adjust/int:subscription_id>/', views.adjust_box, name='adjust_box'),
    # path('<remove/int:subscription_id>/', views.remove_from_box, name='remove_from_box'),
]
