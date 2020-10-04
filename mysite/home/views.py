import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

import home.models

from home.models import Settings

from product.models import catagory

from product.models import product

from home.forms import SearchForm

from product.models import Images

from product.models import Comment


def index(request):
    setting=Settings.objects.get(pk=1)
    category=catagory.objects.all()
    products_slider=product.objects.all().order_by('?')[:4]
    products_latest=product.objects.all().order_by('-id')[:4]
    products_picked=product.objects.all().order_by('?')[:4]
    page="home"
    context={'setting':setting,
             'page':page,
             'products_slider':products_slider,
             'products_latest':products_latest,
             'products_picked':products_picked,
             'category':category}
    return render(request,'index.html',context)

def aboutus(request):
    setting=Settings.objects.get( pk=1 )
    category = catagory.objects.all()
    context={ 'setting':setting ,
              'category':category}
    return render(request,'about.html',context)
def contactus(request):
    setting=Settings.objects.get(pk=1)
    category = catagory.objects.all()
    context={'setting':setting,'category':category}
    return render(request,'contact.html',context)

def category_products(request,id,slug):
    category=catagory.objects.all()
    catdata=product.objects.filter(catagory_id=id)
    products=product.objects.filter(catagory_id=id)
    context = {
               'products' :products,
               'category': category,
     'catdata':catdata}
    return render(request, 'category_products.html', context)

def search(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            query=form.cleaned_data['query']
            catid=form.cleaned_data['catid']
            if catid==0:
                Products=product.objects.filter(title__icontains=query)
            else:
                Products = product.objects.filter(title__icontains=query,catagory_id=catid)
            Category=catagory.objects.all()
            context={'products':Products,'query':query,'category': Category}
            return render(request,'search_products.html',context)
    return HttpResponseRedirect('/')


def search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    products = product.objects.filter(title__icontains=q)
    results = []
    for rs in products:
      product_json = {}
      product_json = rs.title
      results.append(product_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def product_detail(request,id,slug):
    category=catagory.objects.all()
    Product=product.objects.get(pk=id)
    images=Images.objects.filter(product_id=id)
    comments=Comment.objects.filter(product_id=id,status='True')

    context = {
                'Product' :Product,
                'category': category,
                'images': images,
                 'comments':comments
      }
    return render(request, 'product_detail.html', context)



