from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from addresses.models import Addresses
from addresses.serializers import AddressesSerializer
from addresses.utils import *


def home_view(*args, **kwargs):
    return HttpResponse('''
                        <h1>
                            <a href="generate/btc">generate new BTC address (you can choose ETH or DOT also)</a><br>
                            <a href="list/">list addresses</a><br>
                            <a href="address/1">get address</a><br>
                        </h1>
                        ''')


def generate_address(request, currency):
    try:
        addresses = Addresses()

        if currency.lower() == 'btc':
            code = generate_btc_address()
        elif currency.lower() == 'eth':
            code = generate_eth_address()
        elif currency.lower() == 'dot':
            code = generate_dot_address()
        else:
            return JsonResponse({'message': 'Only BTC, ETH or DOT are supported.'})

        # insert address in db
        addresses.address = code
        addresses.currency = currency
        addresses.save()

        return JsonResponse({'address': code})

    except Exception as e:
        return Response(f'Error: {e}')


@api_view(['GET'])
def get_list(request):
    try:
        if request.method == 'GET':
            addresses_list = Addresses.objects.all()
            serializer = AddressesSerializer(addresses_list, many=True)
            return Response(serializer.data)

    except Exception as e:
        return Response(f'Error: {e}')


@api_view(['GET'])
def get_address(request, address_id):
    try:
        address = Addresses.objects.get(id=address_id)
        serializer = AddressesSerializer(address, many=False)
        return Response(serializer.data)

    except Exception as e:
        return Response(f'Error: {e}')
