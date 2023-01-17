from datetime import datetime, timedelta
from http.client import HTTPException
from django.core.exceptions import ValidationError
from rest_framework import generics, permissions
from http import HTTPStatus
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView
import requests
import json
from django.conf import settings
from ..models import *
from .serializers import *


def process_payment(data):

    payment_id = data['data']['id']
    # Obtener información del pago utilizando la API de Mercado Pago
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {'content-type': 'application/json', 'Authorization': f"Bearer {settings.MP_ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    payment_info = json.loads(response.text)
    payment_id = payment_info['id']
    order_id = payment_info['external_reference']

    # Actualizar el estado del pedido en base a la información recibida

    order = Order.objects.get(pk=order_id)
    order.payment_id = payment_id
    order.payment_status = payment_info['status']

    for item in order.items.all():

        prod = Product.objects.prefetch_related('sizes').get(id=item.product_id)
        current_qty = getattr(prod.sizes, item.size)

        if current_qty < item.quantity:
            order.payment_status = 'Stock insuficiente'
            prod.in_stock = False
            continue

        setattr(prod.sizes, item.size, current_qty - item.quantity)

        if not prod.get_sizes_stock():
            prod.is_active = False
            prod.in_stock = False

        # actualizo stock
        prod.sizes.save()
        prod.save()


    order.save()

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
            # "notification_url": f"{request.get_host()}/payments/",
            "notification_url": f"https://0938-181-97-224-45.sa.ngrok.io/api/v1/payments/",
            "statement_descriptor": "SODAN Clothes",
            "expires": True,
            "expiration_date_from": expiration_date_from.isoformat(),
            "expiration_date_to": expiration_date_to.isoformat(),
            "external_reference": order.id,
            # "metadata": {'order_id': order.id},

        }

        __import__('pprint').pprint(preference_data)

        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)


        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        checkout_url = preference['init_point']

        return Response(checkout_url, status=HTTPStatus.OK)
    
        
class PaymentView(APIView):


    def post(self, request, *args, **kwargs):

        # __import__('wdb').set_trace()

        data = json.loads(request.body)
        if data['type'] == 'payment':
        # if data['type'] == 'test':
            if data['action'] == 'payment.created':
            # if data['action'] == 'test.created':
                process_payment(data)
            return Response(HTTP_202_ACCEPTED)
        else:
            #redirigir al usuario a la página de fallo
            return HTTPException('Error. El pago ha fallado!')

