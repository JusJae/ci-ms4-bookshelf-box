from django.urls import path
from . import views


urlpatterns = [
    path('', views.create_subscription, name='subscriptions'),
    path('<int:pk>/', views.view_subscription, name='view_subscription')
]
