from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionOptionForm
from .models import UserSubscriptionOption, SubscriptionOption
from profiles.models import UserProfile

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def how_it_works(request):
    """ A view to show how the site works and subscription plans """
    category_prices = {
        'Childrens': 7.50,
        'Classics': 15.0,
        'Fantasy': 12.50,
        'Fiction': 10.00,
        'Horror': 15.00,
        'Humor': 10.00,
        'Non-Fiction': 12.50,
        'Young Adult': 10.00,
    }
    context = {
        'category_prices': category_prices
    }
    return render(request, 'home/how_it_works.html', context)


@login_required
def create_subscription(request):
    if request.method == 'GET':
        form = SubscriptionOptionForm()
    elif request.method == 'POST':
        form = SubscriptionOptionForm(request.POST)
        if form.is_valid():
            # subscription_option = form.save(commit=False)
            # subscription_option.user = request.user
            # subscription_option.save()
            category = form.cleaned_data['category']
            number_of_books = form.cleaned_data['number_of_books']
            subscription_type = form.cleaned_data['subscription_type']

            # Try to find a matching subscription option
            try:
                subscription_option = SubscriptionOption.objects.get(
                    category=category,
                    number_of_books=number_of_books,
                    subscription_type=subscription_type
                )
                print(f"Debug - Found matching subscription option: {subscription_option}")
            except SubscriptionOption.DoesNotExist:
                messages.error(
                    request, 'Subscription option does not exist. '
                             'Please try again.')
                return redirect('create_subscription')

            user_subscription = UserSubscriptionOption(
                user=request.user,
                subscription_option=subscription_option
            )
            user_subscription.save()
            user_subscription.select_books()
            user_subscription.calculate_and_save_price()

            # Debugging information
            print(f"Debug - Created UserSubscriptionOption with ID: {user_subscription.id}")

            # Store the subscription option in the session
            if 'box' not in request.session:
                request.session['box'] = {}
            request.session['box']['user_subscription_option'] = user_subscription.id
            request.session['box']['subscription_type'] = subscription_option.subscription_type
            request.session.modified = True

            print("Debug - Session data after creating subscription:",
                  request.session['box'])  # Debugging

            messages.success(
                request, 'Subscription option selected successfully.')
            return redirect('checkout')

        else:
            messages.error(
                request, 'Subscription creation failed. '
                         'Please ensure the form is valid.')
    else:
        form = SubscriptionOptionForm()

    return render(request, 'subscriptions/create_subscription.html',
                  {'form': form})


@login_required
def view_subscription(request, pk):
    user_subscription = get_object_or_404(UserSubscriptionOption, pk=pk)
    return render(request, 'subscriptions/view_subscription.html',
                  {'user_subscription': user_subscription})


@login_required
def update_subscription(request, subscription_id):
    """ Update the user's subscription."""
    user_subscription = get_object_or_404(
        UserSubscriptionOption, id=subscription_id, user=request.user)

    if request.method == 'POST':
        form = SubscriptionOptionForm(
            request.POST, instance=user_subscription.subscription_option)
        if form.is_valid():
            subscription_option = form.save()

            try:
                stripe.Subscription.modify(
                    user_subscription.stripe_subscription_id,
                    items=[{
                        'id': user_subscription.stripe_subscription_item_id,
                        'price': subscription_option.stripe_price_id,
                    }]
                )
                user_subscription.subscription_option = subscription_option
                user_subscription.save()
                messages.success(request, 'Subscription updated successfully')
                return redirect('profile')
            except stripe.error.StripeError as e:
                messages.error(request, f'Failed to update subscription: {e}')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        form = SubscriptionOptionForm(
            instance=user_subscription.subscription_option)

    context = {
        'form': form,
        'user_subscription': user_subscription,
    }

    return render(request, 'subscriptions/update_subscription.html', context)
