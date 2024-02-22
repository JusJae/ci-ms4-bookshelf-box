from django.shortcuts import render, redirect, reverse
from django.contrib import messages
# from django.conf import settings

from .forms import OrderForm

# import stripe


def checkout(request):
    box = request.session.get('box', {})
    print("Debug - Box contents:", box)
    if not box:
        messages.error(request, "There's nothing in your box at the moment")
    # return redirect(reverse('subscriptions'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        # 'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        # 'client_secret': intent.client_secret,
    }
    
    return render(request, template, context)
