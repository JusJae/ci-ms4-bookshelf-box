from django.db import models


# Handles the subscription options
class SubscriptionOption(models.Model):
    subscription_types = [
        ('one-off', 'One-off'),
        ('three_months', '3-months'),
        ('six_months', '6-months'),
        ('twelve_months', '12-months'),
    ]
    category = models.ForeignKey(
        'books.Category', on_delete=models.CASCADE)
    number_of_books = models.IntegerField()
    subscription_type = models.CharField(
        max_length=20, choices=subscription_types, default='one-off')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category} - {self.subscription_type}"
