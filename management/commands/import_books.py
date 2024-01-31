# Place this inside a file in: your_app/management/commands/import_books.py

# from django.core.management.base import BaseCommand
# import csv
# from books.models import Books, Category


# class Command(BaseCommand):
#     help = 'Import books from a CSV file'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str,
#                             help='Path to the CSV file with book data')

#     def handle(self, *args, **options):
#         with open(options['csv_file'], newline='') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 category, _ = Category.objects.get_or_create(
#                     name=row['category_name'])
#                 Books.objects.create(
#                     title=row['title'],
#                     author=row['author'],
#                     image_url=row['image_url'],
#                     rating=row['rating'],
#                     description=row['description'],
#                     UPC=row['upc'],
#                     price=row['price'],
#                     availability=row['availability'],
#                     reviews=row['reviews'],
#                     category=category
#                 )
