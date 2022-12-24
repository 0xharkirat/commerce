from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist, Bid, Comment


def index(request):

    totalwatchlist = None

    loggeduser = User.objects.filter(pk=request.user.id).first()

    if loggeduser:

        totalwatchlist = loggeduser.watchlist.all().count()
        

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "totalwatchlist": totalwatchlist
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
        category = request.POST["category"].lower()

        listing = Listing(title=title, description=description, bid=bid, image=image, category=category, user=user)

        listing.save()

        return HttpResponseRedirect(reverse("index"))




    return render(request, "auctions/create.html")

def listing(request, listing_id):
        message = None
        totalwatchlist = None
        

        listing = Listing.objects.get(pk=listing_id)
        comments = listing.listingComments.all()


        loggeduser = User.objects.filter(pk=request.user.id).first()
        canremove=False
        
        if (loggeduser):
            totalwatchlist = loggeduser.watchlist.all().count()
            for user in listing.users.all():
                if user.user.id == loggeduser.id:
                    canremove = True
                    break
            
            
            currentbid =  loggeduser.bids.filter(listing=listing, isCurrent=True)
            totalbids = listing.bids.all().count()
            message = f"{totalbids} bid(s) so far."
            if currentbid:
                message +=  " Your bid is the current bid."

                
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "canremove": canremove,
            "message": message,
            "comments": comments,
            "totalwatchlist": totalwatchlist
           
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


@login_required(login_url='/login')
def bid(request, listing_id):
    if request.method == 'POST':

        user = User.objects.get(pk=request.user.id)
        listing = Listing.objects.get(pk=listing_id)
        bid = float(request.POST["bid"])

        if bid > listing.bid:

            previousbid = Bid.objects.filter(listing=listing, isCurrent=True).first()
            if previousbid:

                previousbid.isCurrent = False
                previousbid.save()

            newbid = Bid(user=user, listing=listing, bid=bid)
            listing.bid = bid
            listing.save()
            newbid.save()

            
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    

@login_required(login_url='/login')
def win(request, listing_id):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)          
        listing = Listing.objects.get(pk=int(request.POST["id"]))

        if user == listing.user:
            winner = listing.bids.filter(isCurrent=True).first()
            if winner:
                listing.winner = winner.user
                listing.isActive = False
                listing.save()

    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required(login_url='/login')
def comment(request, listing_id):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        listing = Listing.objects.get(pk=int(request.POST["id"]))

        comment = request.POST["comment"]

        newComment = Comment(user=user, listing=listing, comment=comment)
        newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))



@login_required(login_url='/login')
def watchlist(request):
    user = User.objects.get(pk=request.user.id)

    watchlist = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


@login_required(login_url='/login')
def categories(request):

    categoriesSet = set()
    categories = Listing.objects.values('category')

    for category in categories:
        categoriesSet.add(category["category"])
    

    print(categoriesSet)

    return render(request, "auctions/categories.html", {
        "categories": categoriesSet,
    })

@login_required(login_url='/login')
def category(request, category):

    

    if category == "general":

        listings = Listing.objects.filter(category="")
    
    else:
        listings = Listing.objects.filter(category=category)

    

    

    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category
    })


                






