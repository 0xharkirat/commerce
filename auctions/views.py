from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

@login_required(login_url='/login')
def create(request):
    if request.method == "POST":

        user = User.objects.get(pk=request.user.id)
        title = request.POST["title"]
        description = request.POST["description"]
        bid = float(request.POST["bid"])
        image = request.POST["image"]
        category = request.POST["category"]

        listing = Listing(title=title, description=description, bid=bid, image=image, category=category, user=user)

        listing.save()

        return HttpResponseRedirect(reverse("index"))




    return render(request, "auctions/create.html")

def listing(request, listing_id):

        listing = Listing.objects.get(pk=listing_id)


        loggeduser = User.objects.filter(pk=request.user.id).first()
        canremove=False
        
        if (loggeduser):
            for user in listing.users.all():
                if user.user.id == loggeduser.id:
                    canremove = True
                    break
                
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "canremove": canremove
        })


@login_required(login_url='/login')
def addWatchlist(request, listing_id):
    if request.method == "POST":

        user = User.objects.get(pk=request.user.id)
        listing = Listing.objects.get(pk=int(request.POST["id"]))
        watchlist = Watchlist(user = user, listing=listing)
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required(login_url='/login')
def removeWatchlist(request, listing_id):
    if request.method == "POST":

        user = User.objects.get(pk=request.user.id)
        listing = Listing.objects.get(pk=int(request.POST["id"]))
        watchlist = Watchlist.objects.get(user = user, listing=listing)
        watchlist.delete()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


