from rest_framework.viewsets import ModelViewSet
from .models import (
    Customer,
    Address,
    City,
    Promotion,
    Collection,
    Product,
    Order,
    OrderItem
)
from .serializers import (
    CustomerSerializer,
    AddressSerializer,
    CitySerializer,
    PromotionSerializer,
    CollectionSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer
)

# Weather API
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

# ----------------------------
#     API VIEWS
# ----------------------------
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_pk']
        return Address.objects.filter(customer_id=customer_id)

    def perform_create(self, serializer):
        customer_id = self.kwargs['customer_pk']
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise NotFound('Customer not found')
        serializer.save(customer=customer)


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs['customer_pk'])


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs['order_pk'])