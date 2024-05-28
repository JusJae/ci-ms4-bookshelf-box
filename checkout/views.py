from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from subscriptions.models import UserSubscriptionOption
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from boxes.contexts import box_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
        pid = json_data.get('client_secret').split('_secret')[0]
        save_info = json_data.get('save_info', False)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        username = request.user.username if request.user.is_authenticated else "AnonymousUser"

        metadata = {
            'box': json.dumps(request.session.get('box', {})),
            'save_info': save_info,
            'username': username,
        }

        if 'subscription_id' in request.session:
            metadata['subscription_id'] = request.session['subscription_id']

        stripe.PaymentIntent.modify(pid, metadata=metadata)
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """ A view to return the checkout page """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':

        box = request.session.get('box', {})
        print("Debug - Box contents:", box)
        if not box:
            messages.error(
                request, "There's nothing in your box at the moment")
            return redirect(reverse('subscriptions'))

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_box = json.dumps(box)
            order.save()

            try:
                for subscription_id, details in box:
                    subscription = UserSubscriptionOption.objects.get(
                        pk=subscription_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        user_subscription_option=subscription,
                        lineitem_total=subscription.calculated_price
                    )
                    order_line_item.save()
                    if 'books' in details:
                        order_line_item.selected_books.set(details['books'])

            except UserSubscriptionOption.DoesNotExist:
                messages.error(request, 'There was an error with your order. \
                        Please try again later.')
                order.delete()
                return redirect(reverse('subscriptions'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        box = request.session.get('box', {})
        if not box:
            messages.error(
                request, "There's nothing in your box at the moment")
            return redirect(reverse('subscriptions'))

        current_box = box_contents(request)
        total = current_box['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ A view to handle successful checkouts """

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    subscriptions_books = {}

    for lineitem in order.lineitems.all():
        subscription_identifier = lineitem.user_subscription_option.subscription_option.subscription_type
        books = lineitem.user_subscription_option.selected_books.all()

        if subscription_identifier not in subscriptions_books:
            subscriptions_books[subscription_identifier] = books
        else:
            subscriptions_books[subscription_identifier].extend(books)

        # subscriptions_books[subscription_identifier].extend(list(lineitem.user_subscription_option.selected_books.all()))

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

    # Save the user's info
    if save_info:
        profile_data = {
            # we set the profile data to the order data
            'default_phone_number': order.phone_number,
            'default_country': order.country,
            'default_postcode': order.postcode,
            'default_town_or_city': order.town_or_city,
            'default_street_address1': order.street_address1,
            'default_street_address2': order.street_address2,
            'default_county': order.county,
        }
        # we create a user profile form instance with the profile data
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        # we save the user profile form
        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'box' in request.session:
        del request.session['box']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'subscriptions_books': subscriptions_books,
    }

    return render(request, template, context)
