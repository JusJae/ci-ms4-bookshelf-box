from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from subscriptions.models import SubscriptionOption, UserSubscriptionOption


def box_contents(request):
    box_items = []
    total = 0
    box_count = 0
    subscription_type = "one-off"

    if request.user.is_authenticated:
        box = request.session.get('box', {})
        user_subscription_id = box.get('user_subscription_option')

        if user_subscription_id:
            user_subscription = get_object_or_404(UserSubscriptionOption, pk=user_subscription_id)
            subscription_option = user_subscription.subscription_option
            if subscription_option:
                subscription_type = subscription_option.subscription_type
                total += user_subscription.calculated_price or 0
                box_count += 1
                selected_books = user_subscription.selected_books.all()
                box_items.append({
                    'user_subscription': user_subscription,
                    'subscription_option': subscription_option,
                    'selected_books': list(selected_books),
                })
        # user_subscriptions = UserSubscriptionOption.objects.filter(
        #     user=request.user, is_active=True)
        # if user_subscriptions.exists():
        #     user_subscription = user_subscriptions.order_by('-start_date').first()
        #     subscription_option = user_subscription.subscription_option
        #     if subscription_option:
        #         subscription_type = subscription_option.subscription_type
        #         total += user_subscription.calculated_price or 0
        #         box_count += 1
        #         selected_books = user_subscription.selected_books.all()
        #         box_items.append({
        #             'subscription_option_id': subscription_option.id,
        #             'subscription_option': subscription_option,
        #             'selected_books': list(selected_books),
        #         })
            # Enhanced debugging prints
            print("Debug - Subscription Option ID:", subscription_option.id)
            print("Debug - Subscription Type:", subscription_type)
    #         else:
    #             print("Debug - No subscription option found.")
    #     else:
    #         print("Debug - No active user subscriptions found.")
    # else:
    #     print("Debug - User not authenticated.")

    # box = request.session.get('box', {})
    # subscription_option_id = box.get('subscription_option')

    # if subscription_option_id:
    #     subscription_option = get_object_or_404(
    #         SubscriptionOption, id=subscription_option_id)
    #     box_count += 1
    #     selected_books = subscription_option.selected_books.all()
    #     box_items.append({
    #         'subscription_option_id': subscription_option_id,
    #         'subscription_option': subscription_option,
    #         'selected_books': list(selected_books),
    #     })

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
