from rest_framework import serializers
from addresses.models import Addresses


class AddressesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Addresses
        fields = ['id', 'address', 'currency']
