from django.db import models

CURRENCY_CHOICES = [
    ('usd', 'USD'),
    ('eur', 'EUR'),
]

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return self.name
    
class Discount(models.Model):
    name = models.CharField(max_length=200)
    stripe_coupon_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=200)
    stripe_tax_id = models.CharField(max_length=200)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem')
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Order {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
