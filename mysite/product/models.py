from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django import forms
# Create your models here.
from django.db.models import Count, Avg
from django.forms import ModelForm, forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput

from user.models import UserProfile

class catagory(MPTTModel):
    STATUS = (
        ('true', 'true'),
        ('false', 'false')
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])


class product(models.Model):
    STATUS = (
        ('true', 'true'),
        ('false', 'false')

    )
    catagory = models.ForeignKey(catagory, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    detail = RichTextUploadingField()  # models.textfields ()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS,default='true')

    # parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.sort_description = 'Image'

    def get_absolute_url(self):
            return reverse('category_detail', kwargs={'slug': self.slug})
    def averagereview(self):
        reviews=Comment.objects.filter(product=self,status='True').aggregate(average=Avg('rate'))
        avg=0
        if reviews["average"] is not None:
                avg=float(reviews["average"])
        return  avg

    def countreview(self):
        reviews=Comment.objects.filter(product=self,status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews ["count"] is not None:
            cnt=int (reviews["count"])
        return cnt



class Images(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def _str_(self):
        return self.title


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('true', 'true'),
        ('false', 'false')

    )

    product = models.ForeignKey(product, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50,blank=True)
    comment = models.CharField(max_length=250,blank=True)

    ip = models.CharField(max_length=20,blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="New")

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.subject


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment']
