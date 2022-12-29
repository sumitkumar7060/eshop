from django.db import models
# Create your models here.
from datetime import datetime


class Registration(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=255, null=True)
    mobile = models.BigIntegerField()
    gender = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.first_name


class catagory(models.Model):
    name = models.CharField(max_length=200, null=True)
    images = models.ImageField(upload_to='upload/catagory/')

    def __str__(self):
        return self.name


class product(models.Model):
    pro_name = models.CharField(max_length=50, null=True)
    price = models.IntegerField()
    desc = models.TextField(max_length=200, null=True)
    pro_image = models.ImageField(upload_to='upload/product/')
    catagory = models.ForeignKey(catagory, on_delete=models.CASCADE)

    def __str__(self):
        return self.pro_name


class Order_dtls(models.Model):
    address = models.CharField(max_length=300, null=True)
    mobile = models.BigIntegerField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Registration, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.customer.first_name
