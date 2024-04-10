from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from subscriptions.models import UserSubscriptionOption
from boxes.contexts import box_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        json_data = json.loads(request.body.decode('utf-8'))
        pid = json_data.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'box': json.dumps(request.session.get('box', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """ A view to retuen the checkout page """

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
            order.stripe_pid = pid
            order.original_box = json.dumps(box)
            order.save()
            for 
            try:
                for subscription_id in box:
                    subscription = UserSubscriptionOption.objects.get(
                        pk=subscription_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        user_subscription_option=subscription,
                        lineitem_total=subscription.calculated_price
                    )
                    order_line_item.save()

            except subscription.DoesNotExist:
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

    # we get the save info from the session
    save_info = request.session.get('save_info')
    # we get the order from the previous view
    order = get_object_or_404(Order, order_number=order_number)
    subscriptions_books = {}

    for lineitem in order.lineitems.all():
        print(lineitem)
        print(subscriptions_books.title, subscriptions_books.price)

        subscription_identifier = lineitem.user_subscription_option.subscription_option.subscription_type
        if subscription_identifier not in subscriptions_books:
            subscriptions_books[subscription_identifier] = []

        subscriptions_books[subscription_identifier].extend(list(lineitem.user_subscription_option.selected_books.all()))
    # will need to add in code that has been copied for user profile info
    # we display a success message to the user
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # if the user has a bag in the session, we delete it
    if 'box' in request.session:
        del request.session['box']

    # we render the checkout success template
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'subscriptions_books': subscriptions_books,
    }

    return render(request, template, context)
