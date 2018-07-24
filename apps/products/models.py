from __future__ import unicode_literals
from django.db import models
from apps.customers.models import Customer
import re
import os

ZIP_REGEX = re.compile(r'^[0-9]{5}$')
STATE_REGEX = re.compile(r'^[A-Z]{2}$')

class ProductManager(models.Manager):
    def category_num(self, cat):
        return self.filter(category=cat).count()

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    desc = models.TextField()
    price = models.DecimalField(max_digits= 10, decimal_places=2)
    inventory = models.IntegerField(default=500)
    quantity_sold = models.IntegerField(default=0)
    image = models.ImageField(upload_to='media', default='none.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()
    def __str__(self):
        return self.name

class OrderItem(models.Model):
    item = models.ForeignKey(Product, related_name="orderitem")
    price = models.DecimalField(max_digits= 10, decimal_places=2)
    amount = models.IntegerField()
    def __str__(self):
        return self.item.name

class OrderManager(models.Manager):
    def order_validator(self, postdata):
        errors = {}

        if not postdata['Sfname']:
            errors['Sfname'] = "Please enter a first name"
        if not postdata['Slname']:
            errors['Slname'] = "Please enter a last name"
        if not postdata['Saddress']:
            errors['Saddress'] = "Please enter an address"
        if not postdata['Scity']:
            errors['Scity'] = "Please enter a city"
        if not postdata['Sstate']:
            errors['Sstate'] = "Please enter a state"
        elif not STATE_REGEX.match(postdata['Sstate']):
            errors['Sstate'] = "Please enter a valid abbreviation"
        if not postdata['Szip']:
            errors['Szip'] = "Please enter a zip code"
        elif not ZIP_REGEX.match(postdata['Szip']):
            errors['Szip'] = "Please enter a valid 5 digit zip code"

        if not postdata['Bfname']:
            errors['Bfname'] = "Please enter a first name"
        if not postdata['Blname']:
            errors['Blname'] = "Please enter a last name"
        if not postdata['Baddress']:
            errors['Baddress'] = "Please enter an address"
        if not postdata['Bcity']:
            errors['Bcity'] = "Please enter a city"
        if not postdata['Bstate']:
            errors['Bstate'] = "Please enter a state"
        elif not STATE_REGEX.match(postdata['Bstate']):
            errors['Bstate'] = "Please enter a valid abbreviation"
        if not postdata['Bzip']:
            errors['Bzip'] = "Please enter a zip code"
        elif not ZIP_REGEX.match(postdata['Bzip']):
            errors['Bzip'] = "Please enter a valid 5 digit zip code"
        
        return errors

class Order(models.Model):
    placer = models.ForeignKey(Customer, related_name="placedorders")
    goods = models.ManyToManyField(OrderItem, related_name="whichorders")
    status = models.CharField(max_length=50, default="Just placed")
    total = models.DecimalField(max_digits= 10, decimal_places=2)

    Sfname = models.CharField(max_length=50)
    Slname = models.CharField(max_length=50)
    Saddress = models.CharField(max_length=100)
    Scity = models.CharField(max_length=50)
    Sstate = models.CharField(max_length=2)
    Szip = models.CharField(max_length=5)

    Bfname = models.CharField(max_length=50)
    Blname = models.CharField(max_length=50)
    Baddress = models.CharField(max_length=100)
    Bcity = models.CharField(max_length=50)
    Bstate = models.CharField(max_length=2)
    Bzip = models.CharField(max_length=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()

def handle_uploaded_file(file, filename):
    with open('media/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def _delete_file(path):
    if os.path.isfile(path):
        os.remove(path)