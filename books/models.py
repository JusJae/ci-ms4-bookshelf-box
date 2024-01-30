from django.db import models


# model for categories

# class Category(models.Model):
#     category = models.CharField(max_length=100, primary_key=True)

#     def __str__(self):
#         return self.category


# model for books

# class Book(models.Model):
#     book_id = models.CharField(max_length=10, primary_key=True)
#     title = models.CharField(max_length=100)
#     author = models.CharField(max_length=100)
#     category = models.CharField(max_length=100)
#     description = models.TextField()
#     rating = models.IntegerField()
#     image_url = models.URLField()
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     stock = models.IntegerField()

#     def __str__(self):
#         return self.title
