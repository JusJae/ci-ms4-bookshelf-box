from django.test import TestCase
from decimal import Decimal
from books.models import Category, Book
from subscriptions.models import SubscriptionOption


class GetRandomBooksTestCase(TestCase):
    def setUp(self):
        # Set up a category for the books
        self.category = Category.objects.create(category="Fiction")

    def create_books(self, num_books):
        for i in range(num_books):
            Book.objects.create(
                title=f"Book {i}",
                description=f"Description {i}",
                category=self.category,
                price=Decimal('10.00') + i  # To vary the price a bit
            )

    def print_selected_books(self, books):
        print("Selected books:")
        # print the name of the test case
        print(self._testMethodName)
        for book in books:
            print(f"- {book.title} (Price: {book.price})")

    def test_no_books(self):
        option = SubscriptionOption.objects.create(
            category=self.category,
            number_of_books=1,
            subscription_type='one-off'
        )
        selected_books = option.get_random_books()
        self.assertEqual(len(selected_books), 0)
        self.print_selected_books(selected_books)

    def test_less_books_than_requested(self):
        self.create_books(2)  # Create 2 books
        option = SubscriptionOption.objects.create(
            category=self.category,
            number_of_books=3,  # Request 3 books
            subscription_type='one-off'
        )
        selected_books = option.get_random_books()
        self.assertEqual(len(selected_books), 2)  # Should only get 2 books
        self.print_selected_books(selected_books)

    def test_exactly_number_of_books_requested(self):
        self.create_books(3)  # Create 3 books
        option = SubscriptionOption.objects.create(
            category=self.category,
            number_of_books=3,  # Request 3 books
            subscription_type='one-off'
        )
        selected_books = option.get_random_books()
        self.assertEqual(len(selected_books), 3)
        self.print_selected_books(selected_books)

    def test_more_books_than_requested(self):
        self.create_books(5)  # Create 5 books
        option = SubscriptionOption.objects.create(
            category=self.category,
            number_of_books=3,  # Request 3 books
            subscription_type='one-off'
        )
        selected_books = option.get_random_books()
        # Should still only get 3 books
        self.assertEqual(len(selected_books), 3)
        self.print_selected_books(selected_books)


class SubscriptionOptionTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category="Test Category")
        self.book1 = Book.objects.create(title="Book 1", category=self.category, price=Decimal('12.00'))
        self.book2 = Book.objects.create(title="Book 2", category=self.category, price=Decimal('18.00'))

    def print_selected_books_and_price(self, subscription_option):
        selected_books = subscription_option.get_random_books()
        print(f"\nTest Method: {self._testMethodName}")
        print("Selected books:")
        for book in selected_books:
            print(f"- {book.title} (Price: {book.price})")
        total_price = subscription_option.calculate_price()
        print(f"Total Calculated Price (After Discounts): {total_price}\n")
        return selected_books, total_price

    def test_no_books_selected_base_price(self):
        subscription_option = SubscriptionOption.objects.create(
            category=self.category, number_of_books=0, subscription_type='one-off')
        expected_price = Decimal('0.00')
        _, calculated_price = self.print_selected_books_and_price(subscription_option)
        self.assertEqual(calculated_price, expected_price)

    def test_price_adjustment_for_selected_books(self):
        subscription_option = SubscriptionOption.objects.create(
            category=self.category, number_of_books=2, subscription_type='one-off')
        _, calculated_price = self.print_selected_books_and_price(subscription_option)
        expected_price = self.book1.price + self.book2.price
        self.assertEqual(calculated_price, expected_price)

    def test_discount_application_based_on_subscription_type(self):
        discount_rate = {
            'one-off': Decimal('1.0'),
            'three_months': Decimal('0.9'),
            'six_months': Decimal('0.8'),
            'twelve_months': Decimal('0.7'),
        }
        for sub_type, rate in discount_rate.items():
            with self.subTest(subscription_type=sub_type):
                subscription_option = SubscriptionOption.objects.create(
                    category=self.category, number_of_books=2, subscription_type=sub_type)
                selected_books, calculated_price = self.print_selected_books_and_price(
                    subscription_option)
                print(f"Discount Rate for '{sub_type}': {rate}")
                sum_of_book_prices = sum(book.price for book in selected_books)
                expected_price = sum_of_book_prices * rate  # rate is already a Decimal
                self.assertAlmostEqual(calculated_price, expected_price, places=2,
                                       msg=f"Failed for subscription type: {sub_type}")
