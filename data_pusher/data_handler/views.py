import json
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer

# Account CRED operations
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def account_list(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        account = Account.objects.get(id=request.data['id'])
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        account = Account.objects.get(id=request.data['id'])
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Destination CRED operations
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def destination_list(request):
    if request.method == 'GET':
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            destination = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        destination = Destination.objects.get(id=request.data['id'])
        serializer = DestinationSerializer(destination, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        destination = Destination.objects.get(id=request.data['id'])
        destination.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Get destinations for a given account
@api_view(['GET'])
def get_destinations_for_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        destinations = account.destinations.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)
    except Account.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

# Incoming data handler API
@api_view(['POST'])
def incoming_data(request):
    app_secret_token = request.headers.get('CL-X-TOKEN')
    
    if not app_secret_token:
        return Response({'error': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        account = Account.objects.get(app_secret_token=app_secret_token)
    except Account.DoesNotExist:
        return Response({'error': 'Invalid app secret token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'POST':
        data = request.data
        destinations = account.destinations.all()
        
        for destination in destinations:
            headers = destination.headers
            if destination.http_method == 'GET':
                response = requests.get(destination.url, headers=headers, params=data)
            elif destination.http_method in ['POST', 'PUT']:
                response = requests.request(destination.http_method, destination.url, headers=headers, json=data)
            else:
                continue
            # Log response or handle errors

        return Response({'status': 'Data pushed to destinations'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
