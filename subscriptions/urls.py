from django.urls import path
from . import views


urlpatterns = [
    path('', views.subscription_view, name='subscriptions'),
    path('display-books/<int:subscription_option_id>/', views.display_books, name='display_books')
]
