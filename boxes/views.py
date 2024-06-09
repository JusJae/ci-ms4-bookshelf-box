from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from subscriptions.models import UserSubscriptionOption
from django.contrib.auth.decorators import login_required


def view_box(request):
    """ A view that renders the box contents page """

    return render(request, 'boxes/box.html')


def add_to_box(request, subscription_id):
    subscription = get_object_or_404(
        UserSubscriptionOption, pk=subscription_id)
    print("Subscription: ", subscription)
    selected_books = subscription.selected_books.all()

    # Initialize the session key if it doesn't exist
    if 'box' not in request.session:
        request.session['box'] = {}

    for book in selected_books:
        if book.availability <= 0:
            messages.error(request, f"Sorry, {book.title} is out of stock.")
            return redirect('view_subscription', pk=subscription_id)
        elif book.availability < 3:
            messages.warning(request, f"Hurry! Only {book.availability} copies of {book.title} left in stock.")

        if str(book.id) in request.session['box']:
            if request.session['box'][str(book.id)] + 1 > book.availability:
                messages.error(request, f"Sorry only {book.availability} copies of {book.title} are available.")
                return redirect('view_subscription', pk=subscription_id)
            request.session['box'][str(book.id)] += 1
        else:
            request.session['box'][str(book.id)] = 1

    # Add the subscription ID if it's not already in the session
    if str(subscription_id) not in request.session['box']:
        request.session['box'][str(subscription_id)] = 1
        request.session.modified = True
        messages.success(request, "Subscription added successfully.")
    else:
        messages.info(request, "This subscription is already in your session.")
        print("Box: ", request.session['box'])
        print("Subscription ID: ", subscription_id)

    # Redirect to a specified path or the same page to show confirmation
    # Fallback to home if no redirect_url provided
    return redirect(request.POST.get('redirect_url', reverse('view_subscription', args=[subscription_id])))


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


@login_required
def remove_from_box(request, subscription_id):
    """Remove the subscription from the box"""

    try:
        subscription = get_object_or_404(
            UserSubscriptionOption, pk=subscription_id)
        box = request.session.get('box', {})

        # Remove the subscription ID from the box
        if 'user_subscription_option' in box and box['user_subscription_option'] == subscription_id:
            box.pop('user_subscription_option')
            messages.success(request, f'Removed {subscription.subscription_option} from your box')
        else:
            messages.error(request, 'Subscription not found in your box.')

        # Update the session
        request.session['box'] = box
        return redirect('view_box')
        # return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect('view_box')
        # return HttpResponse(status=500)

# @login_required
# def remove_from_box(request, subscription_id):
#     """ Remove the subscription option from the box """
#     try:
#         box = request.session.get('box', {})
#         if str(subscription_id) in box:
#             del box[str(subscription_id)]
#             request.session['box'] = box
#             request.session.modified = True
#             messages.success(
#                 request, "Subscription option removed successfully.")
#         else:
#             messages.error(
#                 request, "Subscription option not found in your box.")

#         return redirect('view_box')
#     except Exception as e:
#         messages.error(request, f'Error removing subscription option: {e}')
#         return redirect('view_box')
