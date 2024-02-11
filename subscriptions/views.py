from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionOptionForm
from subscriptions.models import UserSubscriptionOption


@login_required
def create_subscription(request):
    if request.method == 'GET':
        form = SubscriptionOptionForm()  # Ensure this does not default to a specific SubscriptionOption

    elif request.method == 'POST':
        form = SubscriptionOptionForm(request.POST)
        if form.is_valid():
            # Save the subscription option
            subscription_option = form.save()
            print("Debug - SubscriptionOption ID being assigned:", subscription_option.id)
            user_subscription = UserSubscriptionOption(user=request.user, subscription_option=subscription_option)
            print("Debug - Before saving UserSubscriptionOption, SubscriptionOption ID:", user_subscription.subscription_option.id)
            user_subscription.save()
            print("Debug - After saving UserSubscriptionOption, SubscriptionOption ID:", user_subscription.subscription_option.id)
            # get the books for the user subscription
            user_subscription.select_books()
            # calculate the price and save it
            user_subscription.calculate_and_save_price()

            messages.success(request, 'Subscription created successfully.')
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
