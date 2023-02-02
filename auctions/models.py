from django.contrib.auth.models import AbstractUser
from django.db import models
from .forms import *
from django import forms

class User(AbstractUser):
    pass

class Item(models.Model):

    Category_Choices = [
        ('miscellaneous', 'Miscellaneous'),
        ('books', 'Books'),
        ('clothing', 'Clothing'),
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('toys', 'Toys'),
        #allow users to create category and make pages look nicer
    ]

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    startingbid = models.DecimalField(max_digits=6, decimal_places=2)
    item_img = models.ImageField(upload_to='images', default='path/to/my/default/image.jpg')
    category = models.CharField(max_length=64, choices=Category_Choices, default='miscellaneous')
    watchlist_user = models.ManyToManyField(User, related_name='watchlists', blank=True)
    is_open = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.title

    def highest_bid(self):
        highest_bid = self.bid_set.latest('amount')
        return highest_bid
    
    def closebid(self):        
        self.is_open = False
        self.save()


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'startingbid', 'item_img','category']   
        

class Bid(models.Model):
    listing = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Comment(models.Model): 
    listing = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=128, default='')
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)