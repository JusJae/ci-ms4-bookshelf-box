from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import UserProfile
from .forms import UserProfileForm

import stripe


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    has_active_subscription = False
    if profile.stripe_customer_id:
        subscriptions = stripe.Subscription.list(customer=profile.stripe_customer_id, status='active')
        has_active_subscription = any(subscriptions.data)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        'has_active_subscription': has_active_subscription,
    }

    return render(request, template, context)
