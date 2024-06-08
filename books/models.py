from django.db import models


# model for categories
class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)  # noqa: E501

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


# model for books
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='books')
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    rating = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField()
    upc = models.CharField(max_length=25, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.CharField(max_length=50)
    reviews = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title
