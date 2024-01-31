from django.core.management.base import BaseCommand
import csv
import re
import decimal
from books.models import Book, Category

# Define a mapping from number words to their numeric equivalents
number_words_to_numbers = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
}


def convert_rating(word):
    """Convert a number word to its numeric value, return None if not found."""
    return number_words_to_numbers.get(word.lower())


class Command(BaseCommand):
    help = 'Import books from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='Path to the CSV file with book data')

    def handle(self, *args, **options):
        with open(options['csv_file'], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_name = row['Category']
                category, created = Category.objects.get_or_create(
                    category=category_name)
                try:
                    rating = convert_rating(row['Rating'])
                except KeyError:
                    rating = None

                availability_text = row['Availability']
                match = re.search(r'\d+', availability_text)
                availability = int(match.group()) if match else 0

                price_text = row['Price'].replace('£', '').strip()
                try:
                    price = decimal.Decimal(price_text)
                except decimal.InvalidOperation:
                    price = 0.00

                # Now call create with the correctly handled rating
                Book.objects.create(
                    title=row['Title'],
                    category=category,
                    image_url=row['Image'],
                    rating=rating,  # Use the processed rating
                    description=row['Description'],
                    upc=row['UPC'],
                    price=price,
                    availability=availability,
                    reviews=int(row['Reviews']) if row['Reviews'] else 0,
                )
