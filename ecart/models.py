from django.db import models

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




