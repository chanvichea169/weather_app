from django.db import models
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Collection(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Promotion(models.Model):
    note = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.note


class Product(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title


class Char1Field(models.CharField):
    def db_type(self, connection):
        return 'char(1)'


class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True, max_length=50)
    phone = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = Char1Field(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return f'{self.street}, {self.city}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
    ]

    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.title}'
