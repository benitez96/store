from rest_framework import serializers
from ..models import *

class ImageSerializer(serializers.ModelSerializer):

    lookup_field = 'image'

    class Meta:
        model = Image
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    
    main_image = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        exclude = ['created_at', 'modified_at', 'stock', 'cost', 'is_active']


class ProductDetailSerializer(serializers.ModelSerializer):

    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        exclude = ['created_at', 'modified_at', 'stock', 'cost', 'is_active']