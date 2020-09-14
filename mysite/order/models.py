from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from product.models import product


class ShopCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    Product=models.ForeignKey(product,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()
    def __self__(self):
        return self.Product

    @property
    def price(self):
        return (self.Product.price)

    @property
    def amount(self):
        return (self.quantity * self.Product.price)

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields=['quantity']

