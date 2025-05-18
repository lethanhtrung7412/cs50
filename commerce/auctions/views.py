from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bidding
from .forms import ListingForm

def index(request):
    listing = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listing
    })

def detail_listing(request, id):
    data = Listing.objects.get(id=id)
    nums_bid = Bidding.objects.filter(item_bidding=id).count()
    return render(request, "auctions/detail.html", {
        "listing": data,
        "nums_of_bid": nums_bid,
    })

def bidding(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == "POST":
        try:
            new_bid_price = float(request.POST["bid_price"])
        except (KeyError, ValueError):
            return render(request, "auctions/detail.html", {
                "listing": listing,
                "error": "Invalid bid amount."
            })
        if new_bid_price > float(listing.bid_price):
            bid = Bidding.objects.create(amount=new_bid_price, item_bidding=listing, bidder_id=request.user)
            bid.save()
            listing.bid_price = new_bid_price
            listing.save()
            return HttpResponseRedirect(reverse('detail_listing', args=[id]))
        else:
            return render(request, "auctions/detail.html", {
                "listing": listing,
                "error": "Your bid must be higher than the current price."
            })

    return render(request, "auctions/detail.html", {
        "listing": listing
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
            return render(request, "auctions/login.html", {
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {"form": form})

def categories_listing(request):
    categories = Category.objects.all()

    return render(request, "auctions/categories.html",{
        "categories": categories
    })