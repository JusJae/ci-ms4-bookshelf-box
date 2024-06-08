from django.db import models
from django.conf import settings
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone
from books.models import Book


class SubscriptionOption(models.Model):
    SUBSCRIPTION_TYPES = [
        ('one-off', 'One-off'),
        ('monthly', 'Monthly'),
        ('three_months', '3-Months'),
    ]
    category = models.ForeignKey('books.Category', on_delete=models.CASCADE)
    number_of_books = models.IntegerField()
    subscription_type = models.CharField(
        max_length=20, choices=SUBSCRIPTION_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    stripe_price_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        human_readable_subscription_type = self.get_subscription_type_display()
        return (
            f"Category: {self.category} | "
            f"{human_readable_subscription_type} | "
            f"Books: {self.number_of_books}"
        )


class UserSubscriptionOption(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_option = models.ForeignKey(
        SubscriptionOption, on_delete=models.CASCADE, related_name='user_subscriptions')
    selected_books = models.ManyToManyField(Book, related_name='subscriptions')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    calculated_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=256, blank=True, null=True)
    stripe_subscription_item_id = models.CharField(max_length=256, blank=True, null=True)

    def set_end_date(self):
        if self.subscription_option.subscription_type == 'one-off':
            self.end_date = self.start_date
        elif self.subscription_option.subscription_type == 'monthly':
            self.end_date = self.start_date + timedelta(days=30)
        elif self.subscription_option.subscription_type == 'three_months':
            self.end_date = self.start_date + timedelta(days=90)
        else:
            raise ValueError("Unrecognized subscription type.")

    def select_books(self):
        books_in_category = Book.objects.filter(
            category=self.subscription_option.category)
        if books_in_category.exists():
            selected_books = random.sample(list(books_in_category), min(
                self.subscription_option.number_of_books, len(books_in_category)))
            self.selected_books.set(selected_books)
            print("Selected books: ", selected_books)

    def calculate_and_save_price(self):

        category_prices = {
            'Childrens': Decimal('7.50'),
            'Classics': Decimal('15.0'),
            'Fantasy': Decimal('12.50'),
            'Fiction': Decimal('10.00'),
            'Horror': Decimal('15.00'),
            'Humor': Decimal('10.00'),
            'Non-Fiction': Decimal('12.50'),
            'Young Adult': Decimal('10.00'),
        }

        category_name = self.subscription_option.category.category

        price_per_book = category_prices.get(category_name, Decimal('10.00'))

        number_of_books = self.subscription_option.number_of_books
        total_price = price_per_book * number_of_books

        # Apply discount based on subscription type
        discount_rate = {
            'one-off': Decimal('1.0'),  # no discount
            'monthly': Decimal('0.9'),  # 10% discount, not implemented yet
            'three_months': Decimal('0.95'),  # 5% discount
        }
        rate = discount_rate.get(
            self.subscription_option.subscription_type, Decimal('1.0'))

        # Calculate the final price after applying the discount
        self.calculated_price = total_price * rate

        # Save the updated calculated_price field only
        self.save(update_fields=['calculated_price'])

    def save(self, *args, **kwargs):
        # If start date is not set, set it to the current date
        if not self.start_date:
            self.start_date = timezone.now().date()
        if not self.end_date:
            self.set_end_date()
        super(UserSubscriptionOption, self).save(*args, **kwargs)

    def __str__(self):
        return f"Subscription for {self.user.username} - {self.subscription_option}"
