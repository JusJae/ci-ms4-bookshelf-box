from django.http import HttpResponse

from .models import Order, OrderLineItem
from boxes.models import Box

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
        # we return an HTTP response object indicating it was received
        # successfully
        intent = event.data.object
        print(intent)
        pid = intent.id
        box = intent.metadata.box
        save_info = intent.metadata.save_info  # noqa
        stripe_charge = stripe.Charge.retrieve(intent.latest_change)

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)
        print("Debug - Grand Total:", grand_total)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
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
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)

        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    original_box=box,
                    stripe_pid=pid,
                )
                for item_id, quantity in json.loads(box).items():
                    box = Box.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        box=box,
                        quantity=quantity
                    )
                    order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received: {
                event["type"]} | SUCCESS: Verified order already in database',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        # we return an HTTP response object indicating it was received
        # successfully
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
