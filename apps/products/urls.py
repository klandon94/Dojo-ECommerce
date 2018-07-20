from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^showprods$', views.productlist, name="showprods"),
    url(r'^prodpaginate$', views.prodpaginate, name="prodpaginate"),
    url(r'^searchprods$', views.searchprods, name="searchprods"),
    url(r'^sortprods$', views.sortprods, name="sortprods"),
    url(r'^adminprodpaginate$', views.adminprodpaginate, name="adminprodpaginate"),
    url(r'^adminprodsearch$', views.adminprodsearch, name="adminprodsearch"),
    url(r'^adminprodorder$', views.adminprodorder, name="adminprodorder"),
]