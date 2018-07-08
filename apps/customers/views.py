from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Customer
from apps.products.models import Product
import bcrypt

def index(req):
    return redirect('mainpage')

def main(req):
    if 'logged_in' not in req.session:
        req.session['logged_in'] = False
    if 'justloggedout' in req.session and req.session['justloggedout'] == True:
        messages.success(req, "You've been successfully logged out", extra_tags='logout')
        req.session['justloggedout'] = False
    if 'badlogin' in req.session and req.session['badlogin'] == True:
        messages.error(req, "You must be logged in to enter this webpage", extra_tags='logout')
        req.session['badlogin'] = False
    if 'shoppingcart' not in req.session:
        req.session['shoppingcart'] = []
    return render(req, 'customers/mainpage.html')

def register(req):
    req.session['first_name'] = req.POST['first_name']
    req.session['last_name'] = req.POST['last_name']
    req.session['reg_email'] = req.POST['reg_email']
    errors = Customer.objects.register_validator(req.POST)
    if len(errors):
        for key,value in errors.items():
            messages.error(req, value, key)
        return redirect('mainpage')
    else:
        hash1 = bcrypt.hashpw(req.POST['reg_password'].encode(), bcrypt.gensalt())
        newcustomer = Customer(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['reg_email'], password=hash1)
        newcustomer.save()
        req.session['customer'] = newcustomer.first_name
        req.session['id'] = newcustomer.id
        req.session['logged_in'] = True
        return redirect('dashboard')

def custlogin(req):
    req.session['login_email'] = req.POST['login_email']
    result = Customer.objects.filter(email=req.POST['login_email'])

    if not req.POST['login_email'] or not req.POST['login_password']:
        messages.error(req, 'Please fill out all fields', extra_tags='login')
    elif len(result):
        if bcrypt.checkpw(req.POST['login_password'].encode(), result[0].password.encode()):
            req.session['customer'] = result[0].first_name
            req.session['id'] = result[0].id
            req.session['logged_in'] = True
            return redirect('dashboard')
        else:
            messages.error(req, 'You could not be logged in...', extra_tags='login')
    else:
        messages.error(req, 'You have not registered', extra_tags='login')
    return redirect('mainpage')

def dashboard(req):
    if 'logged_in' in req.session and req.session['logged_in'] == True:
        catlist = []
        for x in list(Product.objects.values_list('category', flat=True).distinct()):
            catlist.append({"cat":x, "catnum":Product.objects.category_num(x)})
        return render(req, 'customers/products.html', context = {'categories': catlist})
    req.session.clear()
    req.session['badlogin'] = True
    return redirect('mainpage')

def oneprod(req, id):
    return render(req, 'customers/oneproduct.html', context={'prod':Product.objects.get(id=id)})

def purchase(req, id):
    if req.method == 'POST':
        if not req.POST['quantity']:
            messages.error(req, 'Must enter a number', extra_tags='quantity')
        else:
            cart = req.session['shoppingcart']
            cart.append({'item':Product.objects.get(id=id).name, 'price':float(Product.objects.get(id=id).price), 'quantity':req.POST['quantity'], 'total':float("{0:.2f}".format(int(req.POST['quantity'])*float(Product.objects.get(id=id).price)))})
            req.session['shoppingcart'] = cart
            return redirect('shoppingcart')
    return redirect('oneprod', id=id)

def shoppingcart(req):
    cumulative = 0
    if len(req.session['shoppingcart']):
        for x in req.session['shoppingcart']:
            cumulative += x['total']
    return render(req, 'customers/shoppingcart.html', context={'grandtotal':cumulative})

def custlogout(req):
    req.session.clear()
    req.session['justloggedout'] = True
    return redirect('mainpage')