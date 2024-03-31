from django.db import models
from django.conf import settings
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone
from books.models import Book


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic (2 books)'),
        ('standard', 'Standard (3 books)'),
        ('premium', 'Premium (4 books)'),
    ]
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def set_price(self):
        """Set the price based on the plan."""
        price_mapping = {
            'basic': Decimal('15.00'),
            'standard': Decimal('30.00'),
            'premium': Decimal('45.00'),
        }
        self.price = price_mapping.get(self.name, Decimal('0.00'))

    def save(self, *args, **kwargs):
        self.set_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

    @property
    def number_of_books(self):
        """Return the number of books based on the plan."""
        plan_book_mapping = {
            'basic': 2,
            'standard': 3,
            'premium': 4,
        }
        return plan_book_mapping.get(self.name, 0)


class UserSubscriptionOption(models.Model):
    SUBSCRIPTION_TYPES = [
        ('one-off', 'One-off'),
        ('monthly', 'Monthly'),
        ('three_months', 'Every 3 Months'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    # Assuming there's a Category model
    category = models.ForeignKey(
        'books.Category', on_delete=models.CASCADE, null=True, blank=True)
    selected_books = models.ManyToManyField(Book, blank=True)
    subscription_type = models.CharField(
        max_length=100, choices=SUBSCRIPTION_TYPES, default='one-off')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def select_books(self):
        available_books = Book.objects.filter(
            category=self.category, stock__gt=0)
        # Assuming SubscriptionPlan has a number_of_books attribute
        book_count = self.plan.number_of_books

        if available_books.count() >= book_count:
            selected_books = random.sample(list(available_books), book_count)
            self.selected_books.set(selected_books)
        else:
            print(f"Not enough books in the selected category {
                  self.category} to fulfill the subscription plan {self.plan.name}.")
            self.is_active = False

    def calculate_and_save_price(self):
        base_prices = {'basic': Decimal('20.00'), 'standard': Decimal(
            '35.00'), 'premium': Decimal('55.00')}
        # Adjust based on your SubscriptionPlan setup
        plan_price = base_prices.get(self.plan.name, Decimal('0.00'))

        discount_rate = {
            'one-off': Decimal('1.0'), 'monthly': Decimal('0.9'), 'three_months': Decimal('0.8')}
        rate = discount_rate.get(self.subscription_type, Decimal('1.0'))

        self.price = plan_price * rate
        self.save(update_fields=['price'])

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()
        self.set_end_date()
        super().save(*args, **kwargs)
        # Assuming you want to select books and calculate price upon creation
        if 'created' in kwargs and kwargs['created']:
            self.select_books()
            self.calculate_and_save_price()

    def set_end_date(self):
        mapping = {'one-off': 0, 'monthly': 30, 'three_months': 90}
        days = mapping.get(self.subscription_type, 0)
        self.end_date = self.start_date + timedelta(days=days)

    def __str__(self):
        return f"{self.user.username}'s subscription - {self.plan.name}"
