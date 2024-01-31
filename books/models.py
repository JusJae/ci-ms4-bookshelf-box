from django.db import models


# model for categories

# class Category(models.Model):
#     category = models.CharField(max_length=100, unique=True)  # noqa: E501

#     def __str__(self):
#         return self.category


# model for books

# class Books(models.Model):
#     pk = models.CharField(max_length=10, primary_key=True)
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=100)
#     description = models.TextField()
#     rating = models.CharField(max_length=10)
#     image_url = models.URLField(max_length=500)
#     UPC = models.CharField(max_length=20)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     stock = models.CharField(max_length=50)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title

# after making models makemigrations and migrate
