from django.db import models

from store_app.models import Product

# Create your models here.

class Order(models.Model):

    name = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=100, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=100, 
        default='pending', 
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('finished', 'Finished'),
        ]
    )

    total_amount = models.FloatField()
    # payment = models.OneToOneField(Payment)
    # payment_status = models.CharField

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    price = models.TextField()
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.product.name
