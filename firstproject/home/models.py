from cProfile import label
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import DateField



# Create your models here.

class User(AbstractUser): 
    phone_number = models.CharField(max_length=11)
    age = models.IntegerField()
    password = models.CharField(max_length=20, null=False)
    is_employee = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    salary = models.CharField(max_length=20, default='NS')

class Login(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20, null=False)

class Medicine(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    price = models.IntegerField(null=False)
    stock = models.IntegerField(null=False)
    photo_link = models.URLField()
    requested_stock = models.IntegerField(default=0)
    verify_stock = models.IntegerField(default=0)
    sell = models.IntegerField(default=0)
    income = models.IntegerField(default=0)
    discription = models.CharField(max_length=50, null=True)


class Purchase(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    quantity = models.IntegerField(default=1)
    is_requested = models.BooleanField(default=False)
    is_purchced = models.BooleanField(default=False)
    is_cart = models.BooleanField(default=False)
    is_reject = models.BooleanField(default=False)
    is_clear_byUser = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='Cart')
    price = models.IntegerField(default=0)
    date = models.DateField(null=True)


