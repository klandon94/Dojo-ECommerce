from __future__ import unicode_literals
from django.db import models

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