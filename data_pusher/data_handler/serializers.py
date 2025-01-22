from rest_framework import serializers
from .models import Account, Destination

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'account_name', 'app_secret_token', 'website']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'url', 'http_method', 'headers']
