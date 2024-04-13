from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionOptionForm
from .models import UserSubscriptionOption
from profiles.models import get_or_create_stripe_customer


import stripe


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

            # Ensure the user has a Stripe customer ID
            customer_id = get_or_create_stripe_customer(request.user)
            if not customer_id:
                messages.error(request, "Stripe customer creation failed.")
                return redirect('view_subscription', pk=user_subscription.pk)

            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                if subscription_option.subscription_type != "one-off":
                    price_id = subscription_option.get_stripe_price_id()
                    subscription = stripe.Subscription.create(
                        customer=customer_id,
                        items=[{"price": price_id}],
                        expand=["latest_invoice.payment_intent"]
                    )
                    messages.success(request, "Subscription started successfully.")
                else:
                    messages.success(request, "One-off order created successfully.")
            except Exception as e:
                messages.error(request, f"Subscription creation failed: {e}")
                return redirect('view_subscription', pk=user_subscription.pk)
        else:
            messages.error(
                request, 'Subscription creation failed. Please ensure the form is valid.')
    else:
        form = SubscriptionOptionForm()

    return render(request, 'subscriptions/create_subscription.html', {'form': form})


@login_required
def view_subscription(request, pk):
    user_subscription = get_object_or_404(UserSubscriptionOption, pk=pk)
    return render(request, 'subscriptions/view_subscription.html', {'user_subscription': user_subscription})
