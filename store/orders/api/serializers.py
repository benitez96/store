from rest_framework import serializers
from ..models import *

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        exclude = ['order']

class OrderSerilizer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    def create(self, validated_data):
        __import__('ipdb').set_trace()
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        Item.objects.bulk_create(
            [ Item(**item, order_id=order.id) for item in items ]
        )

        return order


    class Meta:
        model = Order
        fields = '__all__'
