
from django.urls import path
from .views import book_list, book_detail


urlpatterns = [
    path('books/', book_list, name='books'),
    path('<int:book_id>/', book_detail, name='book_detail'),
]
