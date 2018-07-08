from django.shortcuts import render,redirect
from .models import Product

def productlist(req):
    category = req.GET['category']
    return render(req, "products/productlist.html", context={'products': Product.objects.filter(category=category), 'category':category})
