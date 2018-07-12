from django.shortcuts import render,redirect
from .models import Product

def productlist(req):
    category = req.GET['category']
    req.session['category'] = category
    number = 1
    return render(req, "products/productlist.html", {'products': Product.objects.filter(category=category)[0:8], 'category':req.session['category'], 'page': number})

def prodpaginate(req):
    number = req.GET['number']
    category = req.session['category']
    if int(number) == 1:
        after = 8
        before = 0
    else:
        before = 8 * (int(number)-1)
        after = 8 * int(number)
    products = Product.objects.filter(category=category)[before:after]
    context = {
        'page': number,
        'products': products,
        'category': category
    }
    return render(req, "products/productlist.html", context)

def searchprods(req):
    keyword = req.POST['custsearch']
    prods = Product.objects.filter(name__startswith=keyword)
    return render(req, "products/allproducts.html", {'products': prods, 'keyword': keyword})

def sortprods(req):
    sorted = req.POST['sort_by']
    orderby = 'name'
    display = 'by name'
    if sorted == 'hilo':
        orderby = '-price'
        display = 'from most to least $$$'
    if sorted == 'lohi':
        orderby = 'price'
        display = 'from least to most $$$'
    prods = Product.objects.order_by(orderby).filter(category=req.session['category'])
    return render(req, "products/sortedproducts.html", {'products':prods, 'display':display})

def adminprodpaginate(req):
    number = req.GET['number']
    if int(number) == 1:
        after = 5
        before = 0
    else:
        before = 5 * (int(number)-1)
        after = 5 * int(number)
    products = Product.objects.all()[before:after]
    context = {
        'page': number,
        'allproducts': products,
    }
    return render(req, "admins/partialprods.html", context)

def adminprodsearch(req):
    keyword = req.POST['adminsearchp']
    prods = Product.objects.filter(name__startswith=keyword)
    return render(req, "admins/partialprods.html", {'allproducts': prods})