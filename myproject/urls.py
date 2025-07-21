from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from weather_app.views import (
    CityViewSet, CustomerViewSet, PromotionViewSet,
    CollectionViewSet, ProductViewSet, OrderViewSet,
    OrderItemViewSet, AddressViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'cities', CityViewSet)
router.register(r'promotions', PromotionViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'products', ProductViewSet)

customers_router = NestedDefaultRouter(router, r'customers', lookup='customer')
customers_router.register(r'addresses', AddressViewSet, basename='customer-addresses')
customers_router.register(r'orders', OrderViewSet, basename='customer-orders')

orders_router = NestedDefaultRouter(customers_router, r'orders', lookup='order')
orders_router.register(r'items', OrderItemViewSet, basename='order-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(customers_router.urls)),
    path('', include(orders_router.urls)),
]
