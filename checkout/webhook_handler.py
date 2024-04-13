from django.http import HttpResponse

from .models import Order, OrderLineItem
from subscriptions.models import UserSubscriptionOption
from profiles.models import UserProfile

import time
import json
import stripe


class StripeWH_Handler:
    """ Handle Stripe webhooks """

    def __init__(self, request):
        self.request = request
        # we assign the request as an attribute of the class
        # so it can be accessed from stripe events

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        # we return an HTTP response object indicating it was received
        # successfully
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        box = intent.metadata.get('box', {})
        save_info = intent.metadata.get('save_info', False)
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        username = intent.metadata.get('username', 'AnonymousUser')

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        if shipping_details and shipping_details.address:
            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    # if it was, we update the profile information
                    profile.default_phone_number = shipping_details.phone
                    profile.default_country = shipping_details.address.country
                    profile.default_postcode = shipping_details.address.postal_code
                    profile.default_town_or_city = shipping_details.address.city
                    profile.default_street_address1 = shipping_details.address.line1  # noqa
                    profile.default_street_address2 = shipping_details.address.line2  # noqa
                    profile.default_county = shipping_details.address.state
                    profile.save()
            except UserProfile.DoesNotExist:
                profile = None
                print(f"UserProfile for username {username} not found.")

        order_exists = False  # we set the order exists variable to false
        attempt = 1  # we set the attempt variable to 1
        while attempt <= 5:  # as long as the attempt is <=5
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_box=box,
                    stripe_pid=pid,
                )
                # we check if the order exists
                order_exists = True
                # if it does, we break out of the loop
                break
            except Order.DoesNotExist:
                # if the order does not exist, we create a delay
                # for 1 second
                # and increment the attempt variable
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: \
                        Verified order already in database',
                    status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=0,
                    original_box=box,
                    stripe_pid=pid,
                )
                for item_id in box.keys():  # json.loads(box).items():
                    subscription = UserSubscriptionOption.objects.get(
                        id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        user_subscription_option=subscription
                    )
                    order_line_item.save()
                    if 'books' in box[item_id]:
                        book_ids = box[item_id]['books']
                        order_line_item.selected_books.set(book_ids)
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)

        return HttpResponse(content=f'Webhook received: {event["type"]} | SUCCESS: Created order in database', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
