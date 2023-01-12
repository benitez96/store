from datetime import datetime, timedelta
from http.client import HTTPException
from django.core.exceptions import ValidationError
from rest_framework import generics, permissions
from http import HTTPStatus
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from ..models import *
from .serializers import *

class OrderView(generics.CreateAPIView):

    serializer_class = OrderSerilizer

    def post(self, request, *args, **kwargs):
        # import wdb; wdb.set_trace()
        data = JSONParser().parse(request)

        for item in data['items']:
            prod = Product.objects.prefetch_related('sizes').get(id=item['id'])
            current_qty = getattr(prod.sizes, item['size'])
            

            if (current_qty < item['quantity']):
                raise ValidationError(f'Operacion no permitida. Insuficiente stock del producto {prod.name}')

            if (prod.price != item['price']):
                raise ValidationError(f'Operacion no permitida. Precio erroneo del producto {prod.name}')


            item['product_id'] = item.pop('id')
        
        order = OrderSerilizer(data=data)
        if order.is_valid():
            order.save()

        order = Order.objects.get(pk=order.data['id'])

        import mercadopago

        expiration_date_from = datetime.now() - timedelta(minutes=1)
        expiration_date_to = datetime.now() + timedelta(minutes=10)

        preference_data = {
            "items": [
                {
                    "id": item.id,
                    "title": item.product_name,
                    "currency_id": "ARS",
                    "picture_url": item.product.main_image(),
                    "description": item.size.upper(),
                    # "category_id": "art",
                    "quantity": int(item.quantity),
                    "unit_price": float(item.price)
                } for item in order.items.select_related()
            ],
            "payer": {
                "name": order.name,
                "surname": order.lastname,
                "email": order.email,
                "identification": {
                    "type": 'DNI' if len(order.dni) <= 8 else 'CUIL',
                    "number": order.dni
                },
                "address": {
                    "street_name": order.street,
                    "street_number": order.street_number or 1,
                    "zip_code": order.zip_code
                }
            },
            # "back_urls": {
            #     "success": "https://www.success.com",
            #     "failure": "http://www.failure.com",
            #     "pending": "http://www.pending.com"
            # },
            # "auto_return": "approved",
            "notification_url": f"{request.get_host()}/payments/",
            "statement_descriptor": "SODAN Clothes",
            "expires": True,
            "expiration_date_from": expiration_date_from.isoformat(),
            "expiration_date_to": expiration_date_to.isoformat(),
            "metadata": {'order_id': order.id},
            # "external_reference": order.id,

        }

        print(preference_data)

        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)


        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        checkout_url = preference['init_point']

        return Response(checkout_url, status=HTTPStatus.OK)
    
        
class PaymentView(APIView):


    def post(self, request, *args, **kwargs):
        # __import__('ipdb').set_trace()
        data = request.data
        print(request, request)
        print('data', data)
        print(request)
        if data['action'] == 'payment_created':
            print('entre')
        payment_id = data.data['id']
# {
#   "id": 12345,
#   "live_mode": true,
#   "type": "payment",
#   "date_created": "2015-03-25T10:04:58.396-04:00",
#   "application_id": 123123123,
#   "user_id": 44444,
#   "version": 1,
#   "api_version": "v1",
#   "action": "payment.created",
#   "data": {
#       "id": "999999999"
#   }
# }

