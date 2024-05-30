from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

import stripe

from .models import UserProfile


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
