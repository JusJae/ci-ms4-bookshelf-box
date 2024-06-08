from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from subscriptions.models import SubscriptionOption, UserSubscriptionOption


def box_contents(request):
    box_items = []
    total = 0
    box_count = 0
    # Default to "one-off" if not authenticated or no active subscription
    subscription_type = "one-off"

    if request.user.is_authenticated:
        user_subscriptions = UserSubscriptionOption.objects.filter(
            user=request.user, is_active=True)
        if user_subscriptions.exists():
            last_subscription = user_subscriptions.last()
            subscription_option = last_subscription.subscription_option
            if subscription_option:  # Check if subscription_option is not None
                subscription_type = subscription_option.subscription_type
                if last_subscription.calculated_price is not None:
                    total += last_subscription.calculated_price
            # Enhanced debugging prints
            print("Debug - Subscription Option ID:", subscription_option.id)
            print("Debug - Subscription Type:", subscription_type)
    #         else:
    #             print("Debug - No subscription option found.")
    #     else:
    #         print("Debug - No active user subscriptions found.")
    # else:
    #     print("Debug - User not authenticated.")

    box = request.session.get('box', {})
    subscription_option_id = box.get('subscription_option')

    if subscription_option_id:
        subscription_option = get_object_or_404(
            UserSubscriptionOption, id=subscription_option_id)
        if subscription_option.calculated_price is not None:
            total += subscription_option.calculated_price
        box_count += 1
        selected_books = subscription_option.selected_books.all()
        box_items.append({
            'subscription_option_id': subscription_option_id,
            'subscription_option': subscription_option,
            'selected_books': list(selected_books),
        })

    delivery = 0
    free_delivery_delta = 0
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
        'subscription_type': subscription_type,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
