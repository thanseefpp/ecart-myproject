from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    category = models.CharField(max_length = 300)
    name = models.CharField(max_length = 300)
    newprice = models.FloatField()
    oldprice = models.FloatField()
    product_quantity = models.IntegerField()
    image = models.CharField(max_length = 2000)
    imagepr1 = models.CharField(max_length = 2000)
    imagepr2 = models.CharField(max_length = 2000)
    imagepr3 = models.CharField(max_length = 2000)
    imagepr4 = models.CharField(max_length = 2000)
    features = models.TextField(max_length=1000, verbose_name ='features')
    description = models.TextField(max_length=1000, verbose_name ='description')

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null =True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.IntegerField(default=0, null=True, blank=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=300,null=True)
    city = models.CharField(max_length=300, null=True)
    state = models.CharField(max_length=300, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address







