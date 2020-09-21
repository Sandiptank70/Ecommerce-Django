from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string
from order.models import ShopCart

from order.models import ShopCartForm

from product.models import catagory, product, Images, Comment

from user.models import UserProfile

from order.models import OrderForm, Order, OrderProduct


def index(request):
    return HttpResponse("order page")

@login_required(login_url='/login')
def addtoshopcart(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user=request.user
    checkproduct=ShopCart.objects.filter(Product_id=id)
    if checkproduct:
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
                data.Product_id=id
                data.quantity=form.cleaned_data['quantity']
                data.save()
        messages.success(request,"add to cart")
        return HttpResponseRedirect(url)
    else:
        if control==1:
            data=ShopCart.objects.get(Product_id=id)
            data.quantity += 1
            data.save()
        else:
            data=ShopCart()
            data.user_id=current_user.id
            data.Product_id=id
            data.quantity =1
            data.save()
        messages.success(request, "add to cart")
        return HttpResponseRedirect(url)
def shopcart(request):
    category = catagory.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in shopcart:
        total += rs.Product.price * rs.quantity
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,

    }
    return render(request,'shopcart_products.html', context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request,"your item Delete From shopcart")
    return HttpResponseRedirect("/shopcart")


def orderproduct(request):
    category = catagory.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.Product.price * rs.quantity
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()

            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.save()
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                Product = product.objects.get(id=rs.product_id)
                Product.amount -= rs.quantity
                Product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "your order cpmlt")
            return render(request, 'order_Completed.html', {'ordercode': ordercode, 'category': category,})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")
    form = OrderForm()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return render(request,'order_form.html',context)

