from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

import home.models

from home.models import Settings

from product.models import catagory

from product.models import product

from home.forms import SearchForm


def index(request):
    setting=Settings.objects.get(pk=1)
    category=catagory.objects.all()
    products_slider=product.objects.all().order_by('id')[:4]
    products_latest=product.objects.all().order_by('-id')[:4]
    products_picked=product.objects.all().order_by('?')[:4]
    page="home"
    context={'setting':Settings,
             'page':page,
             'products_slider':products_slider,
             'products_latest':products_latest,
             'products_picked':products_picked,
             'category':category}
    return render(request,'index.html',context)

def aboutus(request):
    setting=Settings.objects.get(pk=1)
    context={'setting':Settings}
    return render(request,'about.html',context)
def contactus(request):
    setting=Settings.objects.get(pk=1)
    context={'setting':Settings}
    return render(request,'contact.html',context)

def category_products(request,id,slug):
    category=catagory.objects.all()
    catdata=product.objects.filter(catagory_id=id)
    products=product.objects.filter(catagory_id=id)
    context = {
               'products' :products,
               'category': category}
    return render(request, 'category_products.html', context)

def search(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            query=form.cleaned_data['query']
            catid=form.cleaned_data['catid']
            if catid==0:
                products=product.objects.filter(title_icontains=query)
            else:
                products = product.objects.filter(title_icontains=query,catagory_id=catid)
            category=catagory.objects.all()
            context={'products':products,'category': category}
            return render(request,'search_products.html',context)
    return HttpResponseRedirect('/')



