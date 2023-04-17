from rest_framework import generics, permissions
from ..models import *
from .serializers import *


class ProductView(generics.ListAPIView):

    queryset = Product.objects.filter(in_stock=True, is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):

    lookup_field = 'slug'

    queryset = Product.objects.filter(in_stock=True, is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
