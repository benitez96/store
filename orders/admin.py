from django.contrib import admin

from .models import Item, Order

# Register your models here.

class ItemsAdminStack(admin.StackedInline):
    model = Item




class OrderAdmin(admin.ModelAdmin):

    inlines = [ItemsAdminStack]

    list_display = (
        'name',
        'lastname',
        'email',
        'phone',
        'state',
        'city',
        'street',
        'street_number',
        'neighborhood',
        'shipping_status',
        'shipping_code',
        'payment_status',
        'total_amount',
        'created_at',
        'modified_at'
    )

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)
