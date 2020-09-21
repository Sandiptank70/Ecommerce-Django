from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string
from product.models import catagory

from user.models import UserProfile

from user.forms import SignUpForm

from user.forms import UserUpdateForm, ProfileUpdateForm

from order.models import ShopCart, OrderForm, Order

from order.models import OrderProduct
from product.models import product


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
            userprofile=UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage']=userprofile.image.url
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

@login_required(login_url='/login')
def user_update(request):
    if request.method=='POST':
        user_from=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_from.is_valid() and profile_form.is_valid():
            user_from.save()
            profile_form.save()
            messages.success(request,"your profile update")
            return HttpResponseRedirect('/user')
    else:
        Category = catagory.objects.all()
        user_from = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {'category': Category,
                   'user_from': user_from,
                   'profile_form':profile_form
                   }
        return render(request,'user_update.html',context)

@login_required(login_url='/login')
def user_password(request):

    if request.method=='POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request , user)
            messages.success(request,"Your Password Has Success to Update")
            return HttpResponseRedirect('/user')
        else:
            messages.error(request,'please connect the error below .<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        Category=catagory.objects.all()
        form=PasswordChangeForm(request.user)
        return render(request,'user_password.html',{'form': form,'category': Category})










