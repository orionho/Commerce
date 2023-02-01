from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import ItemForm
from auctions.models import User, Item, Bid, Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from decimal import Decimal

def index(request):
    return render(request, "auctions/index.html", 
    {
        "listings":Item.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", 
            {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", 
            {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", 
            {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    listing = Item.objects.get(id=listing_id) 
    return render(request, "auctions/listing.html",
    {
        "listing": listing 
    })
    
def newlisting(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            listing = form.instance 
            #bid = Bid.objects.create(listing=listing, user=request.user, amount=listing.startingbid)
            return render(request, 'auctions/listing.html', 
            {
                'listing':listing
            })
    else:
        form = ItemForm()
        return render(request, 'auctions/addlisting.html',
        {
            'form': form
        })
        
def display_category(request, category):
    listings = Item.objects.filter(category=category)
    return render(request, 'auctions/listingsbycategory.html',
    {
        'listings': listings
    }) 

@login_required
def watchlist(request):
    user = request.user
    watchlist = Item.objects.filter(watchlist_user=user)
    return render(request, 'auctions/watchlist.html',
    {
        'watchlist':watchlist
    })

@login_required
def add_to_watchlist(request, listing_id):
    user = request.user
    listing = Item.objects.get(id=listing_id)
    listing.watchlist_user.add(user)
    return redirect('watchlist') 
    # change redirect back to listing?

@login_required
def remove_from_watchlist(request, listing_id):
    user = request.user
    listing = Item.objects.get(id=listing_id)
    listing.watchlist_user.remove(user)
    return redirect('watchlist')

def place_bid(request, listing_id):
    listing = Item.objects.get(id=listing_id)
    user = request.user
    bid_amount = Decimal(request.POST.get('bid_amount'))
    try:
        current_price = listing.highest_bid().amount
        if bid_amount > current_price:
            bid = Bid.objects.create(listing=listing, user=user, amount=bid_amount)
            messages.success(request, 'Bid placed successfilly')
        else:
            messages.error(request, 'Bid amount should be greater than the current bid')
        return redirect('listing', listing_id)        
    except:
        current_price = listing.startingbid
        if bid_amount >= current_price:
            bid = Bid.objects.create(listing=listing, user=user, amount=bid_amount)
            messages.success(request, 'Bid placed successfilly')
        else:
            messages.error(request, 'Bid amount should be greater than the starting price.')
        return redirect('listing', listing_id)        

    




    #if bid_amount > listing.highest_bid().amount:
        #bid = Bid.objects.create(listing=listing, user=user, amount=bid_amount)
        #messages.success(request, 'Bid placed successfilly')
    #else:
        #messages.error(request, 'Bid amount should be greater than the current bid')
    #return redirect('listing', listing_id)