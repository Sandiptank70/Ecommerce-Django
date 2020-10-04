from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Settings
from product.models import CommentForm, Comment


def index(request):
    return HttpResponse("mahi patel")

def addcomment(request,id):
    url=request.META.get('HTTP_REFERER')
    # return HttpResponse(url)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            data=Comment()
            data.subject=form.cleaned_data['subject'],
            data.comment=form.cleaned_data['comment'],
            data.ip=request.META.get('REMOTE_ADDR')
            data.product_id=id
            current_user=request.user
            data.user_id=current_user.id
            data.save()
            messages.success(request,"your message is sent . Thank you For Message")
            return HttpResponseRedirect(url)
        else:
            messages.warning(request,"something is wrong")
    return HttpResponseRedirect(url)