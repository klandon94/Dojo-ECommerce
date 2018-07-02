from django.shortcuts import render, redirect
from django.contrib import messages
from apps.customers.models import Customer
from apps.products.models import Product
import bcrypt

def adminmain(req):
    if 'adloggedin' not in req.session:
        req.session['logged_in'] = False
    if 'adloggedout' in req.session and req.session['adloggedout'] == True:
        messages.success(req, "You've been successfully logged out, Mr. Admin", extra_tags='adlogout')
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
    # Product stuff
    # context ...
        return render(req, 'admins/adminorders.html')
    req.session.clear()
    req.session['adbadlogin'] = True
    return redirect('adminmain')

def adminproducts(req):
    if 'adloggedin' in req.session and req.session['adloggedin'] == True:
        return render(req, 'admins/adminproducts.html', context={'allproducts':Product.objects.all()})
    req.session.clear()
    req.session['adbadlogin'] = True
    return redirect('adminmain')

def adminlogout(req):
    req.session.clear()
    req.session['adloggedout'] = True
    return redirect('adminmain')