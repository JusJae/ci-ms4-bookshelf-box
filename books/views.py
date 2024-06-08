from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Book, Category
from .forms import BookForm, StockForm


# book_list
def book_list(request):
    """ A view to show all books, including sorting and search queries """
    books = Book.objects.all()
    query = None
    sort = None
    direction = None
    categories = Category.objects.all()

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            direction = request.GET.get('direction', 'asc')

            if sortkey == 'name':
                sortkey = 'lower_name' if direction == 'asc' else '-lower_name'
                # Assuming 'title' is the field name for book names
                books = books.annotate(lower_name=Lower('title'))
            elif sortkey in ['category', 'price']:
                sortkey = f'{sortkey}' if direction == 'asc' else f'-{sortkey}'
            books = books.order_by(sortkey)

        if 'category' in request.GET:
            category_name = request.GET['category'].split(',')
            books = books.filter(category__category__in=category_name)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('books'))

            queries = Q(title__icontains=query) | Q(
                description__icontains=query)
            books = books.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'books': books,
        'search_term': query,
        'categories': categories,  # Add categories to context
        'current_sorting': current_sorting,
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


# add_book
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('manage_books')
        else:
            messages.error(
                request, 'Failed to add book. Please ensure the form is valid.')
    else:
        form = BookForm()
    context = {
        'form': form,
    }
    return render(request, 'books/add_book.html', context)


# edit_book
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('manage_books')
        else:
            messages.error(
                request, 'Failed to update book. Please ensure the form is valid.')
    else:
        form = BookForm(instance=book)
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'books/edit_book.html', context)


# delete_book
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('manage_books')


# manage_stock
def manage_stock(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock updated successfully!')
            return redirect('manage_books')
        else:
            messages.error(
                request, 'Failed to update stock. Please ensure the form is valid.')
    else:
        form = StockForm(instance=book)
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'books/manage_stock.html', context)
