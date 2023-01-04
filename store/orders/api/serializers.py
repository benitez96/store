from rest_framework import serializers
from ..models import *

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = [ 'product', 'quantity' ]

class OrderSerilizer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
