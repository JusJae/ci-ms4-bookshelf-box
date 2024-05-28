from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.conf import settings
import stripe


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=False)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country', null=True, blank=True)
    has_active_subscription = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update the user profile and create a stripe customer."""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        if not user_profile.stripe_customer_id:
            customer = stripe.Customer.create(email=instance.email)
            user_profile.stripe_customer_id = customer.id
            user_profile.save()
    else:
        # Existing users: just save the profile
        user_profile = instance.userprofile
        if not user_profile.stripe_customer_id:
            customer = stripe.Customer.create(email=instance.email)
            user_profile.stripe_customer_id = customer.id
            user_profile.save()
        # instance.userprofile.save()
