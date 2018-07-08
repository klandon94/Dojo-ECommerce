from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^showprods$', views.productlist, name="showprods")
]