from django.db import models

from store_app.models import Product

# Create your models here.

class Order(models.Model):

    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField()
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
    payment_id = models.CharField(max_length=255)
    payment_status = models.CharField(
        max_length=100, 
        default='pending', 
        choices=[
            ('pending', 'Pending'),
            ('rejected', 'Rejected'),
            ('aproved', 'Aproved'),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=100)
    price = models.TextField()
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.product.name