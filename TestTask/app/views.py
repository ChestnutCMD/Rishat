from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import stripe

from app.models import Item, Discount, Tax, Order, OrderItem
from app.utils import Converter

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_item(request, id):
    """ Создание чекаут сессии на отдельный товар """
    item: Item = get_object_or_404(Item, id=id)
    price: float = item.get_stripe_price(item.price)

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
    """ Эндпоинт успешной оплаты """
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'success.html')


def payment_failed(request):
    """ Эндпоинт неудачной оплаты """
    return render(request, 'cancel.html')


def item_detail(request, id: int):
    """ Эндпоинт отдельного товара пр ID """
    item: Item = get_object_or_404(Item, id=id)
    return render(request, 'item_detail.html', {
        'item': item
    })


def buy_order(request, id: int):
    """ Создание чекаут сессии на группу товаров """
    order: Order = Order.objects.select_related('tax', 'discount').get(id=id)

    total_price: float = OrderItem.objects.filter(order=order).aggregate(
        total_price=Sum(F('item__price') * F('quantity')))['total_price']

    convert_currency = Converter(from_exchange='usd', to_exchange=order.currency, value=total_price)

    tax_rate: stripe.TaxRate = order.tax.create_stripe_tax()
    coupon: stripe.Coupon = order.discount.create_stripe_discount(order.currency)
    price: stripe.Price = order.get_stripe_price(convert_currency.calculation())

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price,
                'quantity': 1,
                "tax_rates": [tax_rate.id]  # Идентификатор налога
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
    """ GET запрос - Эедпоинт всех товаров
    POST запрос - создание заказа Order"""
    if request.method == 'GET':
        items: list[Item] = Item.objects.all()
        return render(request, 'order.html', {'items': items})

    if request.method == 'POST':
        selected_items: list = request.POST.getlist('selected_items')
        selected_currency: str = request.POST.get('selected_currency')
        discount: Discount = Discount.objects.get(id=1)
        tax: Tax = Tax.objects.get(id=1)
        order: Order = Order.objects.create(discount=discount, tax=tax, currency=selected_currency)

        for item_id in selected_items:
            item_quantity = int(request.POST.get(f'item_quantity_{item_id}', 0))
            item: Item = Item.objects.get(pk=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=item_quantity)

        return redirect(f'/order/{order.id}')
