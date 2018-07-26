from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^ecommerce$', views.main, name='mainpage'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.custlogin, name='customerlogin'),
    url(r'^logout$', views.custlogout, name='customerlogout'),
    url(r'^ecommerce/products$', views.dashboard, name='dashboard'),
    url(r'^ecommerce/myorders$', views.myorders, name='myorders'),
    url(r'^ecommerce/cancel/(?P<id>\d+)$', views.cancelord, name='cancelord'),
    url(r'^ecommerce/product/(?P<id>\d+)$', views.oneprod, name='oneprod'),
    url(r'^ecommerce/product/buy/(?P<id>\d+)$', views.purchase, name='purchase'),
    url(r'^ecommerce/shoppingcart$', views.shoppingcart, name='shoppingcart'),
    url(r'^ecommerce/shoppingcart/(?P<word>.+)$', views.cartdelete, name='cartdelete'),
    url(r'^ecommerce/placeorder$', views.placeorder, name='placeorder'),
]