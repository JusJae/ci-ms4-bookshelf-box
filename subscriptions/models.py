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
    name = models.CharField(
        max_length=50, choices=PLAN_CHOICES, default='basic')
    number_of_books = models.IntegerField()
    # plan = models.CharField(
    #     max_length=20, choices=PLAN_CHOICES)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def set_price(self):
        price_mapping = {
            'basic': Decimal('15.00'),
            'standard': Decimal('30.00'),
            'premium': Decimal('45.00'),
        }
        self.price = price_mapping.get(self.plan, Decimal('0.00'))

    def save(self, *args, **kwargs):
        if not self.price:
            self.set_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()


# class SubscriptionOption(models.Model):
#     SUBSCRIPTION_TYPES = [
#         ('one-off', 'One-off'),
#         ('three_months', '3-months'),
#         ('six_months', '6-months'),
#         ('twelve_months', '12-months'),
#     ]
#     category = models.ForeignKey('books.Category', on_delete=models.CASCADE)
#     number_of_books = models.IntegerField()
#     subscription_type = models.CharField(
#         max_length=20, choices=SUBSCRIPTION_TYPES)
#     price = models.DecimalField(
#         max_digits=10, decimal_places=2, null=True, blank=True)

#     # Base price per book
#     base_price_per_book = Decimal('10.00')

#     def __str__(self):
#         human_readable_subscription_type = self.get_subscription_type_display()
#         return (
#             f"Category: {self.category} | "
#             f"{human_readable_subscription_type} | "
#             f"Books: {self.number_of_books}"
#         )


class UserSubscriptionOption(models.Model):
    SUBSCRIPTION_TYPES = [
        ('one-off', 'One-off'),
        ('monthly', 'Monthly'),
        ('three_months', 'Every 3 Months')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey('books.Category', on_delete=models.CASCADE, null=True)
    selected_books = models.ManyToManyField(Book, blank=True)
    subscription_type = models.CharField(max_length=100, choices=SUBSCRIPTION_TYPES, default='one-off')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def set_end_date(self):
        if self.subscription_type == 'one-off':
            self.end_date = self.start_date
        elif self.subscription_type == 'monthly':
            self.end_date = self.start_date + timedelta(days=30)
        elif self.subscription_type == 'three_months':
            self.end_date = self.start_date + timedelta(days=90)
        else:
            raise ValueError("Unrecognized subscription type.")

    # def select_books(self):
    #     books_in_category = Book.objects.filter(
    #         category=self.subscription_option.category)
    #     if books_in_category.exists():
    #         selected_books = random.sample(list(books_in_category), min(
    #             self.subscription_option.number_of_books, len(books_in_category)))
    #         self.selected_books.set(selected_books)
    #         print("Selected books: ", selected_books)

    def select_books(self):
        # Filter books by the selected category and check stock is greater than 0
        available_books = Book.objects.filter(
            category=self.category, stock__gt=0)
        book_count_mapping = {
            'basic': 2,
            'standard': 3,
            'premium': 4}
        book_count = book_count_mapping.get(self.plan.name, 2)  # defaults to 2 if plan not found

        if available_books.count() >= book_count:
            # Select random books from the available books
            selected_books = random.sample(list(available_books), book_count)
            self.selected_books.set(selected_books)
            print("Selected books: ", self.selected_books)
        else:
            # If there are not enough books in the category print a message
            print(f"Not enough books in the selected category {self.category} to fulfill the subscription plan {self.plan.name}.")
            # Set the subscription to inactive
            self.is_active = False

    def calculate_and_save_price(self):
        # Set base prices for subscription plans
        base_prices = {
            'basic': Decimal('20.00'),  # 2 books
            'standard': Decimal('35.00'),  # 3 books
            'premium': Decimal('55.00'),  # 4 books
        }

        # Get the base price for the current subscription plan
        plan_price = base_prices.get(
            self.subscription_option.plan, Decimal('0.00'))

        # Apply discount based on subscription type
        discount_rate = {
            'one-off': Decimal('1.0'),  # no discount
            'monthly': Decimal('0.9'),  # 10% discount
            'three_months': Decimal('0.8'),  # 20% discount
        }

        # Get the rate for the current subscription type
        rate = discount_rate.get(
            self.subscription_option.subscription_type, Decimal('1.0'))

        # Calculate the final price after applying the discount
        self.price = plan_price * rate

        # Save the updated price field only
        self.save(update_fields=['price'])

    def save(self, *args, **kwargs):
        # If start date is not set, set it to the current date
        if not self.start_date:
            self.start_date = timezone.now().date()
        if not self.end_date:
            self.set_end_date()
        super(UserSubscriptionOption, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s {self.plan} subscription"
