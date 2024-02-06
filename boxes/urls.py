from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_box, name='view_box'),
]
