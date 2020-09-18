from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import catagory

from user.models import UserProfile

from user.forms import SignUpForm

@login_required(login_url='/login')
def index(request):

    Category=catagory.objects.all()
    current_user=request.user
    profile=UserProfile.objects.get(user_id=current_user.id)
    context={
        'category': Category,
        'profile':profile

    }
    return render(request,'user_profile.html',context)


def login_form(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            current_user=request.user
            userprofile=UserProfile.objects.filter(user_id=current_user.id)
            # request.session['userimage']=userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error !! username and password incorred")
            return HttpResponseRedirect('/login')


    Category = catagory.objects.all()
    context = {'category': Category}
    return render(request, 'login_form.html',context)

def signup_form(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password =  form.cleaned_data.get('password1')
            user = authenticate( username=username, password=password)
            login(request, user)
            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request,'your acnt crt')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')
    form=SignUpForm()
    Category = catagory.objects.all()
    context = {'category': Category,
               'form':form,
               }
    return render(request,'signup_form.html',context)
def logout_func(request):
    logout (request)
    return HttpResponseRedirect('/')



