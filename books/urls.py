from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='books'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('stock/<int:book_id>/', views.update_stock, name='update_stock'),
]
