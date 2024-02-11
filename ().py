# coding: utf-8
from django.contrib.auth.models import User
from books.models import Book, Category
from subscriptions.models import SubscriptionOption, UserSubsciptionOption
from subscriptions.models import SubscriptionOption, UserSubscriptionOption
user = User.objects.first()
print(user)
category, created = Category.objects.get_or_create(name="Childrens")
category, created = Category.objects.get_or_create(category="Childrens")
from decimal import Decimal
from sunscription.models import SubscriptionOption
from subscription.models import SubscriptionOption
from subscriptions.models import SubscriptionOption
subscription_option, created = SubscriptionOption.objects.get_or_create(
category=category, 
number_of_books=2,
subscription_type='one-off',
)
