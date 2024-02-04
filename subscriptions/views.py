from django.shortcuts import render, redirect
from .forms import SubscriptionOptionForm
from subscriptions.models import SubscriptionOption
from books.models import Book


def subscription_view(request):
    if request.method == 'POST':
        form = SubscriptionOptionForm(request.POST)
        if form.is_valid():
            # Temporary save to calculate price without committing to DB
            temp_option = form.save(commit=False)
            selected_books = temp_option.get_random_books()
            total_price = temp_option.calculate_price()

            # Option 1: Use session to pass data to the next step
            request.session['selected_books_ids'] = [
                book.id for book in selected_books]
            # Convert Decimal to string for session storage
            request.session['total_price'] = str(total_price)

            context = {
                'form': form,
                'total_price': total_price,
                'view_books': True  # Flag to show "View Books" button
                }
            # Redirect to a confirmation page or directly render with context
            # For simplicity, rendering the same page with additional context
            return render(request, 'subscriptions/subscription_form.html', context)
    else:
        form = SubscriptionOptionForm()
    return render(request, 'subscriptions/subscription_form.html', {'form': form})


def display_books(request):
    selected_books_ids = request.session.get('selected_books_ids', [])
    selected_books = Book.objects.filter(id__in=selected_books_ids)
    total_price = request.session.get('total_price', 0)
    return render(request, 'display_books.html', {
        'selected_books': selected_books,
        'total_price': total_price
    })
