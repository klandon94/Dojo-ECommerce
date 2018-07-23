from django.shortcuts import render, redirect
from django.contrib import messages
from apps.customers.models import Customer
from apps.products.models import Product, Order, OrderItem, handle_uploaded_file, _delete_file
import bcrypt

def adminmain(req):
    if 'adloggedin' not in req.session:
        req.session['logged_in'] = False
    if 'adloggedout' in req.session and req.session['adloggedout'] == True:
        messages.success(req, "You've been successfully logged out, Mr. Landon", extra_tags='adlogout')
        req.session['adloggedout'] = False
    if 'adbadlogin' in req.session and req.session['adbadlogin'] == True:
        messages.error(req, "You must be logged in to enter this webpage", extra_tags='adlogout')
        req.session['adbadlogin'] = False
    return render(req, 'admins/adminlogin.html')

def adminlogin(req):
    req.session['admin_email'] = req.POST['admin_email']
    result = Customer.objects.filter(email=req.POST['admin_email'])

    if not req.POST['admin_email'] or not req.POST['adminpw']:
        messages.error(req, 'Please fill out all fields', extra_tags='adlogin')
    elif len(result):
        if bcrypt.checkpw(req.POST['adminpw'].encode(), result[0].password.encode()):
            if result[0].isAdmin == True:
                req.session['admin'] = result[0].first_name
                req.session['adminid'] = result[0].id
                req.session['adloggedin'] = True
                return redirect('adminorders')
            else:
                messages.error(req, 'You do not have admin access!', extra_tags='adlogin')
        else:
            messages.error(req, 'You could not be logged in...', extra_tags='adlogin')
    else:
        messages.error(req, 'You have not registered, and will not be able to obtain admin access anyway. Sorry!', extra_tags='adlogin')
    return redirect('adminmain')

def adminorders(req):
    if 'adloggedin' in req.session and req.session['adloggedin'] == True:
        return render(req, 'admins/adminorders.html', context={'allorders':Order.objects.all()[0:4]})
    req.session.clear()
    req.session['adbadlogin'] = True
    return redirect('adminmain')

def adminord(req, id):
    if 'adloggedin' in req.session and req.session['adloggedin'] == True:
        order = Order.objects.get(id=id)
        tax = float(order.total) * 0.10
        shipping = float(order.total) * 0.05
        grand = float(order.total) + tax + shipping
        items = []
        for x in order.goods.all():
            items.append({"id":x.item.id, "prod":x.item, "price":x.item.price, "quantity":x.amount, "total":round(float(x.amount*x.item.price),2)})
        return render(req, 'admins/adminorder.html', context={'order':order, "items":items, 'tax':round(tax,2), 'shipping':round(shipping,2), 'grand':round(grand,2)})
    req.session.clear()
    req.session['adbadlogin'] = True
    return redirect('adminmain')

def updatestatus(req, id):
    order = Order.objects.get(id=id)
    status = req.POST['newstatus']
    new = ''
    if status == "in_transit":
        new = "In Transit"
    if status == "delivered":
        new = "Delivered"
    if status == "canceled":
        new = "Canceled"
    order.status = new
    order.save()
    return redirect('adminorders')

def adminproducts(req):
    if 'adloggedin' in req.session and req.session['adloggedin'] == True:
        if 'admindelete' in req.session and req.session['admindelete'] == True:
            messages.success(req, "Successfully deleted product", extra_tags="admindelete")
            req.session['admindelete'] = False
        if 'adminadd' in req.session and req.session['adminadd'] == True:
            messages.success(req, "Successfully added a new product", extra_tags="adminadd")
            req.session['adminadd'] = False
        if 'adminedit' in req.session and req.session['adminedit'] == True:
            messages.success(req, "Successfully edited product", extra_tags="adminedit")
            req.session['adminedit'] = False
        return render(req, 'admins/adminproducts.html', context={'allproducts':Product.objects.all()[0:5], 'cats':list(Product.objects.values_list('category', flat=True).distinct())})
    req.session.clear()
    req.session['adbadlogin'] = True
    return redirect('adminmain')

def adminprod(req, id):
    if 'adloggedin' in req.session and req.session['adloggedin'] == True:
        similarprods = []
        prod = Product.objects.get(id=id)
        for x in (Order.objects.filter(goods__item=prod)):
            for y in x.goods.all():
                if y.item != prod:
                    similarprods.append(y.item)
        return render(req, 'admins/adminproduct.html', context={'prod':prod, 'similarprods':similarprods[0:5]})
    req.session.clear()
    req.session['adbadlogin'] = True
    return redirect('adminmain')

def addprod(req):
    if req.POST['addnewcat']:
        category = req.POST['addnewcat']
    else:
        category = req.POST['addcat']
    handle_uploaded_file(req.FILES['newimg'], str(req.FILES['newimg']))
    Product.objects.create(name=req.POST['addname'], category=category, price=float(req.POST['addprice']), desc=req.POST['adddesc'], image=str(req.FILES['newimg']))
    req.session['adminadd'] = True
    return redirect('adminproducts')

def editprod(req, id):
    editprod = Product.objects.get(id=id)
    if req.POST['newcat']:
        category = req.POST['newcat']
    else:
        category = req.POST['editcat']
    if req.FILES['newimg']:
        _delete_file("media/"+str(editprod.image))
        handle_uploaded_file(req.FILES['newimg'], str(req.FILES['newimg']))
        editprod.image = str(req.FILES['newimg'])
    editprod.name = req.POST['editname']
    editprod.desc = req.POST['editdesc']
    editprod.price = round(float(req.POST['editprice']),2)
    editprod.category = category
    editprod.inventory = int(req.POST['editinv'])
    editprod.save()
    req.session['adminedit'] = True
    return redirect('adminproducts')


def deleteprod(req, id):
    if 'adloggedin' in req.session and req.session['adloggedin'] == True:
        deleteprod = Product.objects.get(id=id)
        _delete_file("media/"+str(deleteprod.image))
        deleteprod.delete()
        req.session['admindelete'] = True
        return redirect('adminproducts')
    req.session.clear()
    req.session['adbadlogin'] = True
    return redirect('adminmain')

def adminlogout(req):
    req.session.clear()
    req.session['adloggedout'] = True
    return redirect('adminmain')