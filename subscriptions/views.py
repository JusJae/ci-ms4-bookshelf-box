from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionOptionForm
from .models import UserSubscriptionOption
from profiles.models import UserProfile

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_subscription(request):
    if request.method == 'GET':
        form = SubscriptionOptionForm()

    elif request.method == 'POST':
        form = SubscriptionOptionForm(request.POST)
        if form.is_valid():
            subscription_option = form.save(commit=False)
            subscription_option.user = request.user
            subscription_option.save()

            user_subscription = UserSubscriptionOption(user=request.user, subscription_option=subscription_option)
            user_subscription.save()
            user_subscription.select_books()
            user_subscription.calculate_and_save_price()

            # Store the subscription option in the session
            if 'box' not in request.session:
                request.session['box'] = {}
            request.session['box']['subscription_option'] = user_subscription.id
            request.session['box']['subscription_type'] = user_subscription.subscription_option.subscription_type
            request.session.modified = True

            messages.success(request, 'Subscription option selected successfully. Please proceed to the checkout.')
            return redirect('checkout')

        else:
            messages.error(request, 'Subscription creation failed. Please ensure the form is valid.')
    else:
        form = SubscriptionOptionForm()

    return render(request, 'subscriptions/create_subscription.html', {'form': form})


@login_required
def view_subscription(request, pk):
    user_subscription = get_object_or_404(UserSubscriptionOption, pk=pk)
    return render(request, 'subscriptions/view_subscription.html', {'user_subscription': user_subscription})
