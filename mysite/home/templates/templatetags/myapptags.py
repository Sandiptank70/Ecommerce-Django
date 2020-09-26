from django import template
from django.db.models import Sum
from django.urls import reverse

#from django.conf import settings
from order.models import ShopCart
from product.models import catagory
register=template.Library()

@register.simple_tag
def catagorylist(userid):
    return catagory.objects.all()

@register.simple_tag
def shopcartcount(userid):
    count=ShopCart.objects.count()
    return count

