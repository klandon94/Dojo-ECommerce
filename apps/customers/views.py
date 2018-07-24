from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Customer
from apps.products.models import Product, Order, OrderItem
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
        if 'placedorder' in req.session and req.session['placedorder'] == True:
            messages.success(req, "Successfully placed order", extra_tags="placedorder")
            req.session['placedorder'] = False
        catlist = []
        for x in list(Product.objects.values_list('category', flat=True).distinct()):
            catlist.append({"cat":x, "catnum":Product.objects.category_num(x)})
        return render(req, 'customers/products.html', {'categories': catlist})
    req.session.clear()
    req.session['badlogin'] = True
    return redirect('mainpage')

def myorders(req):
    if 'logged_in' in req.session and req.session['logged_in'] == True:
        myorders = Order.objects.filter(placer=Customer.objects.get(id=req.session['id']))
        return render(req, "customers/myorders.html", {"myorders":myorders})
    req.session.clear()
    req.session['badlogin'] = True
    return redirect('mainpage')

def oneprod(req, id):
    if 'addedcart' in req.session and req.session['addedcart'] == True:
        messages.success(req, "Successfully added to cart", extra_tags="addedcart")
        req.session['addedcart'] = False
    similarprods = []
    prod = Product.objects.get(id=id)
    for x in (Order.objects.filter(goods__item=prod)):
        for y in x.goods.all():
            if y.item != prod:
                similarprods.append(y.item)
    return render(req, 'customers/oneproduct.html', {'prod':prod, 'similarprods': similarprods[0:5]})

def purchase(req, id):
    if req.method == 'POST':
        if not req.POST['quantity']:
            messages.error(req, 'Must enter a number', extra_tags='quantity')
        else:
            cart = req.session['shoppingcart']
            cart.append({'item':Product.objects.get(id=id).name, 'price':float(Product.objects.get(id=id).price), 'quantity':req.POST['quantity'], 'total': round(float(int(req.POST['quantity'])*float(Product.objects.get(id=id).price)),2)})
            req.session['shoppingcart'] = cart
            req.session['addedcart'] = True
            return redirect('oneprod', id=id)
    return redirect('oneprod', id=id)

def shoppingcart(req):
    cumulative = 0
    if len(req.session['shoppingcart']):
        for x in req.session['shoppingcart']:
            cumulative += x['total']
    cumulative = round(cumulative,2)
    return render(req, 'customers/shoppingcart.html', {'grandtotal':cumulative})

def cartdelete(req, word):
    cart = req.session['shoppingcart']
    for x in cart:
        if x['item'] == word:
            cart.remove(x)
    req.session['shoppingcart'] = cart
    return redirect('shoppingcart')

def placeorder(req):
    req.session['Sfname'] = req.POST['Sfname']
    req.session['Slname'] = req.POST['Slname']
    req.session['Saddress'] = req.POST['Saddress']
    req.session['Scity'] = req.POST['Scity']
    req.session['Sstate'] = req.POST['Sstate']
    req.session['Szip'] = req.POST['Szip']

    req.session['Bfname'] = req.POST['Bfname']
    req.session['Blname'] = req.POST['Blname']
    req.session['Baddress'] = req.POST['Baddress']
    req.session['Bcity'] = req.POST['Bcity']
    req.session['Bstate'] = req.POST['Bstate']
    req.session['Bzip'] = req.POST['Bzip']

    if req.method == 'POST':
        errors = Order.objects.order_validator(req.POST)
        if len(errors):
            for key,value in errors.items():
                messages.error(req, value, key)
            return redirect('shoppingcart')
        else:
            user = Customer.objects.get(id=req.session['id'])
            cart = req.session['shoppingcart']
            grand_total = 0
            items = []
            for x in cart:
                prod = Product.objects.get(name=x['item'])
                amt = int(x['quantity'])
                price = x['price']
                prod.inventory -= amt
                prod.quantity_sold += amt
                grand_total += x['total']
                prod.save()
                items.append(OrderItem.objects.create(item=prod, amount=amt, price=price))
            grand_total = round(grand_total, 2)
            neworder = Order.objects.create(placer=user, total=grand_total, Sfname=req.POST['Sfname'], Slname=req.POST['Slname'], Saddress=req.POST['Saddress'], Scity=req.POST['Scity'], Sstate=req.POST['Sstate'], Szip=req.POST['Szip'], Bfname=req.POST['Bfname'], Blname=req.POST['Blname'], Baddress=req.POST['Baddress'], Bcity=req.POST['Bcity'], Bstate=req.POST['Bstate'], Bzip=req.POST['Bzip'])
            for x in items:
                neworder.goods.add(x)
            neworder.save()
            req.session['placedorder'] = True
            req.session['shoppingcart'] = []
            return redirect('dashboard')
            
def custlogout(req):
    req.session.clear()
    req.session['justloggedout'] = True
    return redirect('mainpage')