from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import stripe

from app.models import Item, Discount, Tax, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_item(request, id):
    item = get_object_or_404(Item, id=id)
    price = item.get_stripe_price(item.price)

    checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/payment_success/',
            cancel_url='http://127.0.0.1:8000/payment_failed/',
        )
    return redirect(checkout_session.url, code=303)


def payment_success(request):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'success.html')


def payment_failed(request):
    return render(request, 'cancel.html')


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item_detail.html', {
        'item': item
    })


def buy_order(request, id):
    order = Order.objects.select_related('tax', 'discount').get(id=id)

    total_price = 0
    order_items = OrderItem.objects.filter(order=order)
    for order_item in order_items:
        total_price += order_item.item.price * order_item.quantity

    tax_rate = order.tax.create_stripe_tax()
    coupon = order.discount.create_stripe_discount(order.currency)
    price = order.get_stripe_price(total_price)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price,
                'quantity': 1,
                "tax_rates": [tax_rate.id]
            },
        ],
        discounts=[
            {
                "coupon": coupon.id  # Идентификатор скидочного купона
            }
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/payment_success/',
        cancel_url='http://127.0.0.1:8000/payment_failed/',
    )

    return redirect(checkout_session.url, code=303)


def order_detail(request):
    if request.method == 'GET':
        items = Item.objects.all()
        return render(request, 'order.html', {'items': items})

    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        selected_currency = request.POST.get('selected_currency')
        discount = Discount.objects.get(id=1)
        tax = Tax.objects.get(id=1)
        order = Order.objects.create(discount=discount, tax=tax, currency=selected_currency)

        for item_id in selected_items:
            item_quantity = int(request.POST.get(f'item_quantity_{item_id}', 0))
            item = Item.objects.get(pk=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=item_quantity)

        return redirect(f'/order/{order.id}')
