
from django.urls import path
from .views import ProductList, ProductCreate, ProductRetrieveUpdateDestroy

urlpatterns = [
    path('v1/products/', ProductList.as_view()),
    path('v1/products/new', ProductCreate.as_view()),
    path('v1/products/<int:id>/', ProductRetrieveUpdateDestroy.as_view()),
]
