from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination


class ProductsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('name', 'description',)

    pagination_class = ProductsPagination

    def get_queryset(self):
        available = self.request.query_params.get('available', None)
        if available is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        if available.lower() == 'true':
            return queryset.filter(
                available=available
            )


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = float(request.data.get('price'))
            if price is not None and price <= 0.0:
                raise ValidationError({'price': 'Must be above Ksh 0.00'})
        except ValueError:
            raise ValidationError({'price': 'A valid number is required'})
        return super().create(request, *args, **kwargs)


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('product_data_{}'.format(product_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            product = response.data
            cache.set('product-data_{}'.format(product['id']), {
                'name': product['name'],
                'description': product['description'],
                'price': product['price']
            })
        return response
