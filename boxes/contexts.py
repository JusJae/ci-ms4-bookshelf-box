from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from subscriptions.models import UserSubscriptionOption


def box_contents(request):

    box_items = []
    total = 0
    box_count = 0
    subscription_type = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'subscription_option'):
            subscription_type = request.user.subscription_option.subscription_type
        else:
            subscription_type = "one-off"
    else:
        subscription_type = "one-off"
    box = request.session.get('box', {})

    for subscription_id in box:
        subscription = get_object_or_404(UserSubscriptionOption, pk=subscription_id)
        total += subscription.calculated_price
        box_count += 1
        selected_books = subscription.selected_books.all()
        selected_books_list = list(selected_books) 
        box_items.append({
            'subscription_id': subscription_id,
            'subscription': subscription,
            'selected_books': selected_books_list,
        })

    if subscription_type != "one-off" and total >= settings.FREE_DELIVERY_THRESHOLD:
        delivery = 0
        free_delivery_delta = 0
    else:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total

    grand_total = delivery + total

    context = {
        'box_items': box_items,
        'total': total,
        'box_count': box_count,
        'delivery': delivery,
        # 'subscription_type': subscription_type,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
