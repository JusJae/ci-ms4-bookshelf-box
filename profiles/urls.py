from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('update_subscription/<int:subscription_id>/', views.update_subscription, name='update_subscription'),
    path('delete_subscription/<int:subscription_id>/', views.cancel_subscription, name='cancel_subscription'),
]
