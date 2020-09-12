from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel
from  mptt.fields import TreeForeignKey
class catagory (MPTTModel):
    STATUS = (
        ('true','true'),
        ('false','false')
        )
    parent = TreeForeignKey('self',  blank=True,null=True, related_name='children',on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keyword=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    slug = models.SlugField(null=False,unique=True)
    parent = models.ForeignKey('self',blank=True,null=True,related_name='children', on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


    def __str__(self):
        full_path=[self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return '/'.join(full_path[::-1])


class product(models.Model):
    STATUS = (
        ('true', 'true'),
        ('false', 'false')

    )
    catagory=models.ForeignKey(catagory,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price=models.FloatField()
    amount=models.IntegerField()
    minamount=models.IntegerField()
    detail = RichTextUploadingField()#models.textfields ()
    slug = models.SlugField(null=False,unique=True)
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


class Images(models.Model):
        product = models.ForeignKey(product, on_delete=models.CASCADE)
        title = models.CharField(max_length=50, blank=True)
        image = models.ImageField(blank=True, upload_to='images/')

        def _str_(self):
            return self.title

