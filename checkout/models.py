import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from profiles.models import UserProfile
from books.models import Book
from subscriptions.models import UserSubscriptionOption


class Order(models.Model):
    """ A model to store order information """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=False, blank=True)
    county = models.CharField(max_length=80, null=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_box = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """ Generate a random, unique 32 char order number using UUID """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ Update grand total each time a line item is added,
            accounting for delivery costs """

        self.order_total = (
            self.lineitems.aggregate(
                Sum('lineitem_total'))['lineitem_total__sum'] or 0)
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """ Override the original save method to set the
            order number if it hasn't been set already """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        """ Return the order number as a string """
        return self.order_number


class OrderLineItem(models.Model):
    """ A model to store order line item information """

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    user_subscription_option = models.ForeignKey(
        'subscriptions.UserSubscriptionOption', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='lineitems')
    selected_books = models.ManyToManyField(
        'books.Book', related_name='lineitems')
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """ Override the original save method to set the lineitem total and update the order total """
        if not self.id:
            self.lineitem_total = self.user_subscription_option.calculated_price
        super(OrderLineItem, self).save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        """ Return the subscription order number as a string """
        return f'Subscription for order {self.order.order_number}'
