from django.shortcuts import render, redirect
import requests
from .models import City, Customer, Order, Product, Promotion, Address
from .serializers import CitySerializer, CustomerSerializer, OrderSerializer, ProductSerializer, PromotionSerializer, \
    AddressSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


API_KEY = 'd2b4ca9a1b4bca5ebb28f2e87ae55850'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

def home(request):
    if request.method == 'POST':
        city_name = request.POST.get('city', '').strip()
        if city_name and not City.objects.filter(name__iexact=city_name).exists():
            try:
                response = requests.get(WEATHER_URL.format(city_name, API_KEY)).json()
                if response.get('cod') == 200:
                    City.objects.create(name=city_name)
                else:
                    return render(request, 'index.html', {'error_message': 'City not found.'})
            except requests.RequestException:
                return render(request, 'index.html', {'error_message': 'Failed to connect to weather service.'})

    weather_data = []
    for city in City.objects.all():
        try:
            response = requests.get(WEATHER_URL.format(city.name, API_KEY)).json()
            if response.get('cod') == 200:
                weather_data.append({
                    'city': city.name,
                    'temperature': response['main']['temp'],
                    'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon'],
                })
            else:
                city.delete()
        except requests.RequestException:
            continue

    return render(request, 'index.html', {'weather_data': weather_data})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# ----------------- API Views ------------------

@api_view(['GET'])
def city_list(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def city_detail(request, id):
    try:
        city = City.objects.get(id=id)
        serializer = CitySerializer(city)
        return Response(serializer.data)
    except City.DoesNotExist:
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def order_detail(request, id):
    try:
        order = Order.objects.get(id=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view()
def promotion_list(request):
    promotions = Promotion.objects.all()
    serializer = PromotionSerializer(promotions, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def promotion_details(request, id):
    try:
        promotion = Promotion.objects.get(id=id)
        serializer = PromotionSerializer(promotion)
        return Response(serializer.data)
    except Promotion.DoesNotExist:
        return Response({'error': 'Promotion not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def customer_list(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def customer_detail(request, id):
    try:
        customer = Customer.objects.get(id=id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def promotion_list(request):
    promotions = Promotion.objects.all()
    serializer = PromotionSerializer(promotions, many=True)
    return Response(serializer.data)
@api_view(['GET', 'DELETE', 'PUT'])
def promotion_details(request, id):
    try:
        promotion = Promotion.objects.get(id=id)
    except Promotion.DoesNotExist:
        return Response({'error': 'Promotion not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PromotionSerializer(promotion)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        promotion.delete()
        return Response({'message': 'Promotion deleted'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = PromotionSerializer(promotion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List and Create
@api_view(['GET', 'POST'])
def address_list(request):
    if request.method == 'GET':
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Retrieve, Update, Delete
@api_view(['GET', 'PUT', 'DELETE'])
def address_detail(request, id):
    try:
        address = Address.objects.get(id=id)
    except Address.DoesNotExist:
        return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        address.delete()
        return Response({'message': 'Address deleted'}, status=status.HTTP_204_NO_CONTENT)
