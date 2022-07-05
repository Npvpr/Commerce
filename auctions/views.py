from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

# from .models import User

def index(request):
    listing = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listing": listing,
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def create_listing(request):
    error_message = None
    if request.method == "POST":
        # check required elements from server side
        if not request.POST["item_name"]:
            error_message = "Item Name cannot be empty!"
        elif not request.POST["floor_price"]:
            error_message = "Floor price cannot be empty!"
        else:
            item_name = request.POST["item_name"]
            floor_price = request.POST["floor_price"]

            item_image = request.POST["item_image"]
            description = request.POST["description"]
            item_category = request.POST["item_category"]

            current_user = request.user

            itemq = Item(
                owner=current_user,
                item_name=item_name,
                item_price=floor_price,
                item_image=item_image,
                item_category=item_category
                )
            itemq.save()

            listq = Listing(
                lister=current_user,
                listed_item=itemq,
                description=description,
                floor_price=floor_price
                )
            listq.save()

            return HttpResponseRedirect(reverse("index")) 

    form = CreateListForm()
    return render(request, "auctions/create_listing.html",{
        "error_message": error_message,
        "form": form,
        })

@login_required(login_url='login')
def item_detail(request, element_id, error_message=None):
    
    element = Listing.objects.get(id=element_id)
    current_user = request.user

    try:
        all_bids = Bid.objects.filter(bidded_item=element.listed_item)
        bid_count = all_bids.count()
        current_bidder = all_bids.order_by('-bidded_price').first().bidder
    except:
        bid_count = None
        current_bidder = None

    try:
        comments = Comment.objects.filter(commented_item=element.listed_item)
    except:
        comments = None

    try:
        watched_list_id = Watchlist.objects.get(watcher=current_user, watched_list=element).id
    except:
        watched_list_id = None

    # return HttpResponse(f"{bid_count}")
    return render(request, "auctions/item_detail.html",{
        "error_message": error_message,
        "element": element,
        "current_user": current_user,
        "bid_count": bid_count,
        "current_bidder": current_bidder,
        "comments": comments,
        "watched_list_id": watched_list_id,
        })

@login_required(login_url='login')
def bidding(request):
    error_message = None
    element_id = request.POST["element_id"]
    element = Listing.objects.get(id=element_id)

    current_user = request.user   

    # Check for errors
    if not request.POST["current_bidded_price"]:
        error_message = "Please input the bid price!"
    elif int(request.POST["current_bidded_price"]) <= element.floor_price:
        error_message = "Bid Price must be higher than the floor price or the current bid!"
    elif current_user == element.lister:
        error_message = "Lister Cannot Bid!"
    if error_message:
        return HttpResponseRedirect(reverse('item_detail', kwargs={
            "element_id": element_id,
            "error_message": error_message,
            }))

    current_bidded_price = int(request.POST["current_bidded_price"])

    current_bid = Bid(
        bidder = current_user,
        bidded_item = element.listed_item,
        bidded_price = current_bidded_price
        )
    current_bid.save()

    element.floor_price = current_bidded_price
    element.save()

    itemq = element.listed_item
    itemq.item_price = current_bidded_price
    itemq.save()

    return HttpResponseRedirect(reverse('item_detail', kwargs={
            "element_id": element_id,
            }))

@login_required(login_url='login')
def close_bidding(request):
    error_message = None
    element_id = request.POST["element_id"]
    element = Listing.objects.get(id=element_id)

    current_user = request.user

    current_bidder_id = request.POST["current_bidder_id"]
    current_bidder = User.objects.get(id=current_bidder_id)

    # Check for errors
    if current_user != element.lister:
        error_message = "Only lister can close the bid!"
    if error_message:
        return HttpResponseRedirect(reverse('item_detail', kwargs={
            "element_id": element_id,
            "error_message": error_message,
            }))

    element.sold = True
    element.save()

    itemq = element.listed_item
    itemq.owner = current_bidder
    itemq.save()

    return HttpResponseRedirect(reverse('item_detail', kwargs={
            "element_id": element_id,
            }))

@login_required(login_url='login')
def commenting(request):
    error_message = None
    element_id = request.POST["element_id"]
    commenter_id = request.POST["commenter_id"]
    commented_item_id = request.POST["commented_item_id"]

    # Check for errors
    if not request.POST["comment"]:
        error_message = "You can't comment without Text!"
    if error_message:
        return HttpResponseRedirect(reverse('item_detail', kwargs={
            "element_id": element_id,
            "error_message": error_message,
            }))

    comment = request.POST["comment"]

    commenter = User.objects.get(id=commenter_id)
    commented_item = Item.objects.get(id=commented_item_id)

    commentq = Comment(
        commenter = commenter,
        commented_item = commented_item,
        comment =comment
        )
    commentq.save()

    return HttpResponseRedirect(reverse('item_detail', kwargs={
            "element_id": element_id,
            }))

@login_required(login_url='login')
def watchlist(request):
    current_user = request.user
    try:
        listing_ids = Watchlist.objects.values_list('watched_list', flat=True).filter(watcher=current_user)
        listing = Listing.objects.filter(pk__in=set(listing_ids))
    except:
        listing = None
    return render(request, "auctions/index.html",{
        "listing": listing,
        "watchlist": "Watchlist",
        })

@login_required(login_url='login')
def add_watchlist(request):
    element_id = request.POST["element_id"]
    element = Listing.objects.get(id=element_id)

    current_user = request.user

    addwatchlistq = Watchlist(watcher=current_user, watched_list=element)
    print(addwatchlistq.watched_list)
    addwatchlistq.save()

    return HttpResponseRedirect(reverse('item_detail', kwargs={
            "element_id": element_id,
            }))

@login_required(login_url='login')
def remove_watchlist(request):
    element_id = request.POST["element_id"]
    element = Listing.objects.get(id=element_id)
    watched_list_id = request.POST["watched_list_id"]

    current_user = request.user

    watchlistq = Watchlist.objects.get(id=watched_list_id)
    watchlistq.delete()

    return HttpResponseRedirect(reverse('item_detail', kwargs={
            "element_id": element_id,
            }))

def categories(request):
    categories = Item.objects.values_list('item_category', flat=True).exclude(item_category='').exclude(item_category__isnull=True).distinct()
    return render(request, "auctions/categories.html",{
        "categories": categories,
        })

def category_detail(request, category):
    listed_items = Item.objects.filter(item_category=category)
    listing = Listing.objects.filter(listed_item__in=listed_items)
    return render(request, "auctions/index.html",{
        "listing": listing,
        "category": category,
        })

"""
    - Since Heroku is connected to git repo, whenever commiting changes to git, the database file(sqlite file) kept changing back
"""