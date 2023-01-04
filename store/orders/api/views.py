from rest_framework import generics, permissions
from ..models import *
from .serializers import *

class OrderView(generics.CreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerilizer
    
        