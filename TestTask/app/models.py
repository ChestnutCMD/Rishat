from typing import Optional

from django.db import models
from stripe import Coupon, TaxRate, Price


class BaseModel(models.Model):
    CURRENCY = [('usd', 'usd'), ('rub', 'rub'), ('eur', 'eur')]
    currency = models.CharField(choices=CURRENCY, max_length=3, default='usd')

    def get_stripe_price(self, total_price: Optional[float | int]) -> Price:
        price = Price.create(
            currency=self.currency,
            unit_amount=int(total_price * 100),
            product_data={"name": self.__str__()})
        return price

    class Meta:
        abstract = True


class Item(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Discount(models.Model):
    DURATION = [('once', 'Once'), ('repeating', 'Repeating'), ('forever', 'Forever')]

    name = models.CharField(max_length=255)
    percent_off = models.PositiveIntegerField()
    duration = models.CharField(choices=DURATION, default='once', max_length=9)

    def __str__(self):
        return self.name

    def create_stripe_discount(self, currency: str) -> Coupon:
        coupon = Coupon.create(
            name=self.name,
            currency=currency,
            percent_off=self.percent_off,
            duration=self.duration,
        )
        return coupon

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    display_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    jurisdiction = models.CharField(max_length=20)
    percentage = models.DecimalField(max_digits=5, decimal_places=1)
    inclusive = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name

    def create_stripe_tax(self) -> TaxRate:
        tax_rate = TaxRate.create(
            display_name=self.display_name,
            description=self.description,
            jurisdiction=self.jurisdiction,
            percentage=self.percentage,
            inclusive=self.inclusive
        )
        return tax_rate

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Order(BaseModel):
    items = models.ManyToManyField(Item, through='OrderItem')
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Номер заказа: {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
