from http.client import HTTPException
from django.core.exceptions import ValidationError
from rest_framework import generics, permissions
from http import HTTPStatus
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import *
from .serializers import *

class OrderView(generics.CreateAPIView):

    serializer_class = OrderSerilizer

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)

        for item in data['items']:
            prod = Product.objects.prefetch_related('sizes').get(id=item['id'])
            current_qty = getattr(prod.sizes, item['size'])

            if (current_qty < item['quantity']):
                raise ValidationError(f'Operacion no permitida. Insuficiente stock del producto {prod.name}')


            item['product_id'] = item.pop('id')
            # setattr(prod.sizes, item['size'], current_qty - item['quantity'])

            # prod.sizes.save()

            # prod.in_stock = prod.get_sizes_stock() == 0
            # prod.save()
        
        order = OrderSerilizer(data=data)
        if order.is_valid():
            order.save()

        return Response(status=HTTPStatus.OK)
    
        
