from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SubscriptionOptionForm
from subscriptions.models import UserSubscriptionOption


@login_required
def create_subscription(request):
    print("Method: ", request.method)
    if request.method == 'POST':
        form = SubscriptionOptionForm(request.POST)
        if form.is_valid():
            # Save the subscription option
            subscription_option = form.save()
            # set the start date
            subscription_option.start_date = timezone.now().date()
            # Create a UserSubscription instance linking the subs option to the user
            user_subscription = UserSubscriptionOption(
                user=request.user, subscription_option=subscription_option)
            user_subscription.save()

            messages.success(request, 'Subscription created successfully.')
            return redirect('view_subscription', pk=user_subscription.pk)
        else:
            messages.error(
                request, 'Subscription creation failed. Please ensure the form is valid.')
    else:
        form = SubscriptionOptionForm()

    return render(request, 'subscriptions/create_subscription.html', {'form': form})


def view_subscription(request, pk):
    user_subscription = get_object_or_404(UserSubscriptionOption, pk=pk)
    return render(request, 'subscriptions/view_subscription.html', {'user_subscription': user_subscription})
