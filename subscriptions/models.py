from django.db import models
from decimal import Decimal
import random
from books.models import Book


class SubscriptionOption(models.Model):
    subscription_types = [
        ('one-off', 'One-off'),
        ('three_months', '3-months'),
        ('six_months', '6-months'),
        ('twelve_months', '12-months'),
    ]
    category = models.ForeignKey('books.Category', on_delete=models.CASCADE)
    number_of_books = models.IntegerField()
    subscription_type = models.CharField(
        max_length=20, choices=subscription_types)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    # Base price per book
    base_price_per_book = Decimal('10.00')

    def get_random_books(self):
        books_in_category = Book.objects.filter(category=self.category)
        if books_in_category.exists():
            return random.sample(list(books_in_category), min(len(books_in_category), self.number_of_books))
        else:
            return []

    def calculate_price(self):
        selected_books = self.get_random_books()

        # Calculate initial and actual prices
        initial_price = self.base_price_per_book * \
            Decimal(self.number_of_books)
        actual_price = sum(book.price for book in selected_books)

        # Use the higher of the initial or actual price
        total_price = max(initial_price, actual_price)

        # Apply discount based on subscription type
        discount_rate = {
            'one-off': Decimal('1.0'),  # no discount
            'three_months': Decimal('0.9'),  # 10% discount
            'six_months': Decimal('0.8'),  # 20% discount
            'twelve_months': Decimal('0.7'),  # 30% discount
        }
        rate = discount_rate.get(self.subscription_type, Decimal('1.0'))
        total_price *= rate
        return total_price

    def __str__(self):
        return f"{self.category} - {self.subscription_type}"
