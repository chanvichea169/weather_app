from rest_framework import serializers
from .models import (
    Customer,
    Product,
    Collection,
    Promotion,
    Address,
    City,
    Order,
    OrderItem,
)


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=50, source='name')
    desc = serializers.CharField(max_length=200, source='description')


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'note', 'discount']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'inventory',
            'last_update',
            'collection',
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city']


class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'birth_date',
            'gender',
            'status',
            'addresses'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_date', 'status', 'customer_id', 'items']
        read_only_fields = ['items']

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        customer = Customer.objects.get(pk=customer_id)
        return Order.objects.create(customer=customer, **validated_data)
