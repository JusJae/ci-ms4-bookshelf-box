from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book


# book_list
def book_list(request):
    """ A view to show all books, including sorting and search queries """

    category_name = request.GET.get('category_name')
    books = Book.objects.all()  # Moved this line up for simplification
    if category_name:
        books = books.filter(category__category=category_name)

    query = None
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('books'))

            queries = Q(title__icontains=query) | Q(
                description__icontains=query)
            books = books.filter(queries)

    context = {
        'books': books,
        'search_term': query,
    }

    return render(request, 'books/book_list.html', context)


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
