from django.shortcuts import render,redirect, HttpResponse
from .models import Product, Order
import json

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

def prodinfo(req):
    prod_id = req.GET['prod']
    prod = Product.objects.get(id=prod_id)
    data = {
        'name': prod.name,
        'desc': prod.desc,
        'price': float(prod.price),
        'cat': prod.category,
        'inv': prod.inventory,
    }
    return HttpResponse(json.dumps(data))

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
    return render(req, "admins/partialprods.html", {'page': number, 'allproducts': products})

def adminordpaginate(req):
    number = req.GET['number']
    if int(number) == 1:
        after = 4
        before = 0
    else:
        before = 4 * (int(number)-1)
        after = 4 * int(number)
    orders = Order.objects.all()[before:after]
    return render(req, "admins/partialords.html", {'page':number, 'allorders':orders})
    
def adminprodsearch(req):
    keyword = req.POST['adminsearchp']
    prods = Product.objects.filter(name__startswith=keyword)
    return render(req, "admins/partialprods.html", {'allproducts': prods})

def adminordsearch(req):
    keyword = req.POST['adminsearcho']
    ords = Order.objects.filter(placer__first_name__startswith=keyword)|Order.objects.filter(placer__last_name__startswith=keyword)
    return render(req, "admins/partialords.html", {'allorders': ords})

def adminprodorder(req):
    sorted = req.POST['orderby']
    prods = Product.objects.order_by(sorted)
    return render(req, "admins/partialprods.html", {'allproducts':prods})

def adminordorder(req):
    sorted = req.POST['orderby']
    orderby = 'id'
    if sorted == 'name':
        orderby = 'placer__first_name'
    if sorted == 'price_lo':
        orderby = 'total'
    if sorted == 'price_hi':
        orderby = '-total'
    ords = Order.objects.order_by(orderby)
    return render(req, "admins/partialords.html", {'allorders':ords})