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
   # parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
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
    VARIANTS=(
        ('None','None'),
        ('Size','Size'),
        ('Color','Color'),
        ('Size-Color','Size-Color')
    )
    catagory = models.ForeignKey(catagory, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    variant=models.CharField(max_length=10,choices=VARIANTS,default='None')
    detail = RichTextUploadingField()  # models.textfields ()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)

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
    rate = models.IntegerField(default=1)
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
class Color (models.Model):
    name=models.CharField(max_length=20)
    code=models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color</p>'.format(self.code))
        else:
            return ""
class Size(models.Model):
    name=models.CharField(max_length=20)
    code=models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return self.name

class Variants(models.Model):
    title=models.CharField(max_length=100,blank=True,null=True)
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE,blank=True,null=True)
    size=models.ForeignKey(Size,on_delete=models.CASCADE,blank=True,null=True)
    image_id=models.IntegerField(blank=True,null=True,default=0)
    quantity=models.IntegerField(default=1)
    price=models.FloatField(default=0)
    def __str__(self):
        return self.title
    def image(self):
        img=Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage=img.image.url
        else:
            varimage=""
        return varimage
    def image_tag(self):
        img=Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" heights="50"/>'.format(img.image.url))
        else:
            return ""
