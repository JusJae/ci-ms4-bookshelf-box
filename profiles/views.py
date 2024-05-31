from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import UserProfile
from .forms import UserProfileForm
from subscriptions.models import UserSubscriptionOption

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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

    orders = profile.orders.filter(user_profile=profile)
    active_subscriptions = UserSubscriptionOption.objects.filter(
        user=request.user, is_active=True)

    # has_active_subscription = active_subscriptions.exists()

    has_active_subscription = False
    if profile.stripe_customer_id:
        stripe_subscriptions = stripe.Subscription.list(
            customer=profile.stripe_customer_id, status='active')
        has_active_subscription = any(stripe_subscriptions.data)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'subscriptions': active_subscriptions,
        'on_profile_page': True,
        'has_active_subscription': has_active_subscription,
    }

    return render(request, template, context)


# @login_required
# def update_subscription(request, subscription_id):
#     """ Update the user's subscription. """
#     subscription = get_object_or_404(UserSubscriptionOption, id=subscription_id, user=request.user)

#     if request.method == 'POST':
#         try:
#             stripe.Subscription.modify(
#                 subscription.stripe_subscription_id,
#                 items=[{
#                     'id': subscription.stripe_subscription_item_id,
#                     'price': request.POST['price'],
#                 }]
#             )
#             messages.success(request, 'Subscription updated successfully')
#         except stripe.error.StripeError as e:
#             messages.error(request, f'Failed to update subscription: {e}')

#     return redirect('profile')


@login_required
def cancel_subscription(request, subscription_id):
    """ Cancel the user's subscription. """
    subscription = get_object_or_404(UserSubscriptionOption, id=subscription_id, user=request.user)

    if request.method == 'POST':
        try:
            stripe.Subscription.delete(subscription.stripe_subscription_id)
            subscription.is_active = False
            subscription.save()
            messages.success(request, 'Subscription cancelled successfully')
        except stripe.error.StripeError as e:
            messages.error(request, f'Failed to cancel subscription: {e}')

    return redirect('profile')
