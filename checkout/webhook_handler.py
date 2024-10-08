from django.http import HttpResponse
# from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from subscriptions.models import UserSubscriptionOption
from profiles.models import UserProfile

import time
import json
import stripe
import sendgrid
import os
import logging


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content

logger = logging.getLogger(__name__)


class StripeWH_Handler:
    """ Handle Stripe webhooks """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order, event):
        """Send the user a confirmation email"""

        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        # Create the email content
        from_email = Email(settings.DEFAULT_FROM_EMAIL),
        to_email = Email(cust_email),
        content = Content(body),

        message = Mail(from_email, to_email, subject, content)
        message_json = message.get()

        try:
            sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
            response = sg.client.mail.send.post(request_body=message_json)
            print(response.status_code)
            print(response.headers)

            logger.info(
                f'Email send response status code: {response.status_code}')
            if response.status_code == 202:
                logger.info(f'Email sent successfully to {cust_email}')
                return HttpResponse(content=f'Webhook received: {event["type"]} | SUCCESS: Email sent', status=200)
            else:
                logger.error(
                    f'Failed to send email to {cust_email}: {response.status_code}')
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: Failed to send email', status=500)
        except Exception as e:
            logger.error(f'Error sending email: {e}')
            return HttpResponse(content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ Handle the payment_intent.succeeded webhook from Stripe """
        intent = event.data.object
        pid = intent.id
        metadata = intent.metadata
        box = metadata.get('box', '{}')
        save_info = metadata.get('save_info', 'false') == 'true'
        username = metadata.get('username', 'AnonymousUser')

        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping or {}
        grand_total = round(stripe_charge.amount / 100, 2)

        address = {}

        if 'address' in shipping_details:
            address = shipping_details['address']
        for field, value in address.items():
            if value == "":
                address[field] = None

        # Update profile information if save_info was checked
        profile = None
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.full_name = shipping_details.get('name')
                profile.default_phone_number = shipping_details.get('phone')
                profile.default_country = address.get('country')
                profile.default_postcode = address.get('postal_code')
                profile.default_town_or_city = address.get('city')
                profile.default_street_address1 = address.get('line1')
                profile.default_street_address2 = address.get('line2')
                profile.default_county = address.get('state')
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.get('name', ''),
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.get('phone', ''),
                    country__iexact=address.get('country', ''),
                    postcode__iexact=address.get('postal_code', ''),
                    town_or_city__iexact=address.get('city', ''),
                    street_address1__iexact=address.get('line1', ''),
                    street_address2__iexact=address.get('line2', ''),
                    county__iexact=address.get('state', ''),
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
            self._send_confirmation_email(order, event["type"])
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: \
                        Verified order already in database',
                    status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.get('name', ''),
                    user_profile=profile,
                    email=billing_details.get('email', ''),
                    phone_number=shipping_details.get('phone', ''),
                    country=address.get('country', ''),
                    postcode=address.get('postal_code', ''),
                    town_or_city=address.get('city', ''),
                    street_address1=address.get('line1', ''),
                    street_address2=address.get('line2', ''),
                    county=address.get('state', ''),
                    grand_total=0,
                    original_box=box,
                    stripe_pid=pid,
                )

                for item_id, item_data in json.loads(box).items():
                    subscription = UserSubscriptionOption.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        user_subscription_option=subscription
                    )
                    order_line_item.save()
                    if 'books' in item_data:
                        book_ids = item_data['books']
                        order_line_item.selected_books.set(book_ids)
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)

        self._send_confirmation_email(order, event["type"])
        return HttpResponse(content=f'Webhook received: {event["type"]} | SUCCESS: Created order in database', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_subscription_created(self, event):
        subscription = event['data']['object']
        customer_id = subscription['customer']
        stripe_subscription_id = subscription['id']
        try:
            user_subscription = UserSubscriptionOption.objects.filter(user__userprofile__stripe_customer_id=customer_id).latest('start_date')
            user_subscription.stripe_subscription_id = stripe_subscription_id
            user_subscription.save()
            print(f"Subscription {stripe_subscription_id} created for customer {customer_id}")
            # Send subscription confirmation email
            order = Order.objects.create(
                user_profile=user_subscription.user.userprofile,
                email=user_subscription.user.email if hasattr(user_subscription.user, 'email') else user_subscription.user.userprofile.email,
                full_name=user_subscription.user.get_full_name(),
                grand_total=user_subscription.price,
                stripe_pid=stripe_subscription_id,
            )
            self._send_confirmation_email(order, event["type"])
        except UserSubscriptionOption.DoesNotExist:
            print(f"No matching UserSubscriptionOption found for customer {customer_id}")
        return HttpResponse(status=200)

    def handle_subscription_updated(self, event):
        subscription = event['data']['object']
        stripe_subscription_id = subscription['id']
        # Update subscription details in your database
        try:
            user_subscription = UserSubscriptionOption.objects.get(stripe_subscription_id=stripe_subscription_id)
            user_subscription.calculate_and_save_price()
            user_subscription.is_active = True
            user_subscription.save()
            print(f"Subscription {stripe_subscription_id} has been updated.")
        except UserSubscriptionOption.DoesNotExist:
            print(f"No matching UserSubscriptionOption found for subscription {stripe_subscription_id}")
        return HttpResponse(status=200)

    def handle_subscription_deleted(self, event):
        subscription = event['data']['object']
        stripe_subscription_id = subscription['id']
        try:
            user_subscription = UserSubscriptionOption.objects.get(stripe_subscription_id=stripe_subscription_id)
            user_subscription.is_active = False
            user_subscription.save()
            print(f"Subscription {stripe_subscription_id} has been cancelled.")
        except UserSubscriptionOption.DoesNotExist:
            print(f"No matching UserSubscriptionOption found for subscription {stripe_subscription_id}")
        return HttpResponse(status=200)

    def create_order_from_intent(intent):
        order = Order.objects.create(
            stripe_pid=intent['id'],
            full_name="Obtained from intent or customer record",
            total=intent['amount_received'] / 100,
            status='completed',
        )
        return order
