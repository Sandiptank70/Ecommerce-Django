from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import catagory

from user.models import UserProfile


def index(request):
    return HttpResponse("user app ")


def login_form(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            current_user=request.user
            userprofile=UserProfile.objects.filter(user_id=current_user.id)
            request.session['userimage']=userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error !! username and password incorred")
            return HttpResponseRedirect('/login')


    Category = catagory.objects.all()
    context = {'category': Category}
    return render(request, 'login_form.html',context)

def signup_form(request):
    Category = catagory.objects.all()
    context = {'category': Category}
    return HttpResponse("signup form")


