from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Item, Order, OrderItem, Discount, Tax

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        order = form.instance
        currencies = set(order.items.values_list('currency', flat=True))
        if len(currencies) > 1:
            raise ValidationError('Все товары в заказе должны быть одной валюты!')

admin.site.register(Item)
admin.site.register(Discount)
admin.site.register(Tax)
admin.site.register(Order, OrderAdmin)