from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Item, Order
import stripe
from django.conf import settings

def get_item(request, id):
    item = get_object_or_404(Item, pk=id)
    if item.currency == 'usd':
        publishable_key = settings.STRIPE_PUBLISHABLE_KEY_USD
    else:
        publishable_key = settings.STRIPE_PUBLISHABLE_KEY_EUR
    return render(request, 'shop/item.html', {'item': item, 'publishable_key': publishable_key})

def get_buy(request, id):
    item = get_object_or_404(Item, pk=id)
    if item.currency == 'usd':
        stripe.api_key = settings.STRIPE_SECRET_KEY_USD
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY_EUR

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {'name': item.name},
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'{settings.SITE_URL}/success/',
        cancel_url=f'{settings.SITE_URL}/cancel/',
    )

    return JsonResponse({'session_id': session.id})

def get_order_buy(request, id):
    order = get_object_or_404(Order, pk=id)
    order_items = order.orderitem_set.all()

    # Определяем валюту по первому товару в заказе
    first_item = order_items.first().item
    if first_item.currency == 'usd':
        stripe.api_key = settings.STRIPE_SECRET_KEY_USD
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY_EUR

    line_items = []
    for order_item in order_items:
        line_item = {
            'price_data': {
                'currency': order_item.item.currency,
                'product_data': {'name': order_item.item.name},
                'unit_amount': int(order_item.item.price * 100),
            },
            'quantity': order_item.quantity,
        }
        if order.tax:
            line_item['tax_rates'] = [order.tax.stripe_tax_id]
        line_items.append(line_item)

    session_params = {
        'payment_method_types': ['card'],
        'line_items': line_items,
        'mode': 'payment',
        'success_url': f'{settings.SITE_URL}/success/',
        'cancel_url': f'{settings.SITE_URL}/cancel/',
    }

    if order.discount:
        session_params['discounts'] = [{'coupon': order.discount.stripe_coupon_id}]

    session = stripe.checkout.Session.create(**session_params)
    return JsonResponse({'session_id': session.id})

def get_payment_intent(request, id):
    item = get_object_or_404(Item, pk=id)
    if item.currency == 'usd':
        stripe.api_key = settings.STRIPE_SECRET_KEY_USD
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY_EUR

    intent = stripe.PaymentIntent.create(
        amount=int(item.price * 100),
        currency=item.currency,
        metadata={'item_id': item.id},
    )

    return JsonResponse({'client_secret': intent.client_secret})
