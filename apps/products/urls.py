from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^showprods$', views.productlist, name="showprods"),
    url(r'^prodpaginate$', views.prodpaginate, name="prodpaginate"),
    url(r'^searchprods$', views.searchprods, name="searchprods"),
    url(r'^sortprods$', views.sortprods, name="sortprods"),
]