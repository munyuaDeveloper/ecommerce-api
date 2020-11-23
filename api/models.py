from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='products-images')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name
