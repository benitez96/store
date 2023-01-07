from rest_framework import serializers
from ..models import *


class SizesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sizes
        exclude = ['id', 'product']


class ProductSerializer(serializers.ModelSerializer):
    
    main_image = serializers.StringRelatedField(read_only=True)
    sizes = SizesSerializer()

    class Meta:
        model = Product
        exclude = ['created_at', 'modified_at', 'cost', 'is_active']


class ProductDetailSerializer(serializers.ModelSerializer):

    images = serializers.StringRelatedField(many=True)
    sizes = SizesSerializer()

    class Meta:
        model = Product
        exclude = ['created_at', 'modified_at', 'cost', 'is_active', 'slug']

