from decimal import Decimal
from django.conf import settings


def box_content(request):

    box_items = []
    total = 0
    box_count = 0
    subscription_type = None
    if request.user.is_authenticated:
        subscription_type = request.user.user_subscription
    # Assuming the subscription type is stored in the user object

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
