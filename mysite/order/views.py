from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from order.models import ShopCart

from order.models import ShopCartForm


def index(request):
    return HttpResponse("order page")

@login_required(login_url='/login')
def addtoshopcart(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user=request.user
    checkout=ShopCart.objects.filter(Product_id=id)
    if(checkout):
        control=1
    else:
        control=0

    if request.method == 'POST':
        form=ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                data=ShopCart.objects.get(Product_id=id)
                data.quantity +=form.cleaned_data['quantity']
                data.save()
            else:
                data=ShopCart()
                data.user_id=current_user.id
                data.product_id=id
                data.quantity=form.cleaned_data['quantity']
                data.save()
        messages.success(request,"add to cart")
        return HttpResponseRedirect(url)
    else:
        if control==1:
            data=ShopCart.objects.get(product_id=id)
            data.quantity+=1
            data.save()
        else:
            data=ShopCart()
            data.user_id=current_user.id
            data.product_id=id
            data.quantity =1
            data.save()
        messages.success(request, "add to cart")
        return HttpResponseRedirect(url)