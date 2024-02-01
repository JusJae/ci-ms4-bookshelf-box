from django.shortcuts import get_object_or_404, render
from .models import Book


# book_list
def book_list(request):
    books = Book.objects.all()

    return render(request, 'books/book_list.html', {'books': books})


# views that need to be created for the books app:
# book_details
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'books/book_detail.html', context)

# search_books
# add_book
# edit_book
# delete_book
# list_categories
