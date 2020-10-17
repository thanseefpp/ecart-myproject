from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    category = models.CharField(max_length = 300)
    name = models.CharField(max_length = 300)
    newprice = models.FloatField()
    oldprice = models.FloatField()
    product_quantity = models.IntegerField()
    image_url = models.ImageField(null=True, blank=True)
    imagefull_1 = models.ImageField(null=True, blank=True)
    imagefull_2 = models.ImageField(null=True, blank=True)
    imagefull_3 = models.ImageField(null=True, blank=True)
    imagefull_4 = models.ImageField(null=True, blank=True)
    features = models.TextField(max_length=1000, verbose_name ='features')
    description = models.TextField(max_length=1000, verbose_name ='description')

    @property
    def ImageURL(self):
        try:
            url = self.image_url.url
        except:
            url = ''
        return url

    @property
    def ImageURLFULL(self):
        try:
            url = self.imagefull_1.url
        except:
            url = ''
        return url

    @property
    def ImageURLFULLTWO(self):
        try:
            url = self.imagefull_2.url
        except:
            url = ''
        return url

    @property
    def ImageURLFULLTT(self):
        try:
            url = self.imagefull_3.url
        except:
            url = ''
        return url

    @property
    def ImageURLFULLTF(self):
        try:
            url = self.imagefull_4.url
        except:
            url = ''
        return url


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
    order_status = models.CharField(default = 'Pending',max_length=200,null=True)
    
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.newprice * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=300,null=True)
    city = models.CharField(max_length=300, null=True)
    state = models.CharField(max_length=300, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=300, null=True)
    payment_Cod = models.CharField(max_length=300, null=True)
    def __str__(self):
        return self.address

    







