from django.urls import path
from . import views


urlpatterns = [
    path('', views.create_subscription, name='subscriptions'),
    path('<int:pk>/', views.view_subscription, name='view_subscription'),
    path('how_it_works/', views.how_it_works, name='how_it_works'),
    path(
        'update/<int:subscription_id>/',
        views.update_subscription,
        name='update_subscription'
    ),
    path(
        'cancel/<int:subscription_id>/',
        views.cancel_subscription,
        name='cancel_subscription'
    ),
]
