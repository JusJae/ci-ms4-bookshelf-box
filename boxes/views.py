from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from subscriptions.models import SubscriptionOption, UserSubscriptionOption
from django.contrib.auth.decorators import login_required


def view_box(request):
    """ A view that renders the box contents page """

    return render(request, 'boxes/box.html')


# # def add_to_box(request, pk):
#     """ Add user subscription option to box content """
#     subscription = get_object_or_404(UserSubscriptionOption, pk=pk)
#     # redirect_url = request.POST.get('redirect_url')
#     box = request.session.get('box', {})
    
#     if pk in box:
#         box[pk] += 1
#         messages.success(request, f'Added another {subscription.name} to your box')
#     else:
#         box[pk] = 1
#         messages.success(request, f'Added {subscription.name} to your box')
    
#     request.session['box'] = box
#     print(request.session['box'])
#     # return redirect(redirect_url)
#     return redirect('view_subscription', pk=pk)


def add_to_box(request, subscription_id):
    subscription = get_object_or_404(
        UserSubscriptionOption, pk=subscription_id)
    print("Subscription: ", subscription)

    # Initialize the session key if it doesn't exist
    if 'box' not in request.session:
        request.session['box'] = []

    # Add the subscription ID if it's not already in the session
    if subscription_id not in request.session['box']:
        request.session['box'].append(subscription_id)
        request.session.modified = True  # Make sure Django saves the session change
        messages.success(request, "Subscription added successfully.")
    else:
        messages.info(request, "This subscription is already in your session.")
        print("Box: ", request.session['box'])
        print("Subscription ID: ", subscription_id)

    # Redirect to a specified path or the same page to show confirmation
    # Fallback to home if no redirect_url provided
    return redirect(request.POST.get('redirect_url', '/'))


# def adjust_box(request, subscription_id):
#     """Adjust the quantity of the specified subscription to the specified amount"""

#     subscription = get_object_or_404(
#         UserSubscriptionOption, pk=subscription_id)
#     quantity = int(request.POST.get('quantity'))
#     box = request.session.get('box', {})

#     if quantity > 0:
#         box[subscription_id] = quantity
#         messages.success(request, f'Updated {subscription.name} quantity to {quantity}')
#     else:
#         box.pop(subscription_id)
#         messages.success(request, f'Removed {subscription.name} from your box')

#     request.session['box'] = box
#     return redirect('view_box')


# def remove_from_box(request, subscription_id):
#     """Remove the subscription from the box"""

#     try:
#         subscription = get_object_or_404(
#             UserSubscriptionOption, pk=subscription_id)
#         box = request.session.get('box', {})

#         box.pop(subscription_id)
#         messages.success(request, f'Removed {subscription.name} from your box')

#         request.session['box'] = box
#         return redirect('view_box')
#         # return HttpResponse(status=200)

#     except Exception as e:
#         messages.error(request, f'Error removing item: {e}')
#         return redirect('view_box')
#         # return HttpResponse(status=500)
