from django.shortcuts import render
from .models import Book


# book_list
def book_list(request):
    books = Book.objects.all()

    return render(request, 'books/book_list.html', {'books': books})


# views that need to be created for the books app:
# book_details
# search_books
# add_book
# edit_book
# delete_book
# list_categories
