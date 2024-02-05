from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='books'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
]
