from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import models
from .forms import ListingForm, CommentForm, RegisterForm, BidForm
from .models import User, Listing, Comment, Article_list

import os
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

os.environ['DJANGO_SETTINGS_MODULE'] = 'adoptions.settings'


def index(request):
    # Home page will only show active listings.
    listings = Listing.objects.all().filter(status=Listing.ACTIVE).order_by(
        '-listing_date'
    )
    # When logged in, get the users watchlist in order to toggle the
    # Watchlist/Remove button on active listings.
    if request.user.is_authenticated:
        user_watchlist = User.objects.get(
            pk=int(request.user.id)).watchlist.all()
        return render(request, "auctions/index.html",
                      {"listings": listings,
                       "watchlist": user_watchlist})
    return render(request, "auctions/index.html", {"listings": listings})


@require_http_methods(["POST"])
def place_bid(request):
    top_bid = 0
    try:
        bid_listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")

    if bid_listing.top_bid():
        top_bid = int(bid_listing.top_bid().bid)
    # BidForm will validate the new bid against top_bid and
    # min_bid data provided to BidForm constructor.
    form = BidForm(request.POST,
                   min_bid=int(bid_listing.min_bid),
                   top_bid=top_bid)
    if form.is_valid():
        try:
            # Create a BidModel from the form,
            # add Listing and User data before saving the Bid
            new_bid = form.save(commit=False)
            new_bid.listing = bid_listing
            new_bid.owner = request.user
            new_bid.save()
        except IntegrityError:
            messages.add_message(request, messages.WARNING,
                                 "We were unable to place your entry.")
            return HttpResponseRedirect(
                reverse("listing", args=(bid_listing.id,)))
        # Saving the bid was successful
        messages.add_message(request, messages.SUCCESS,
                             "Your entry was successful.")
        return HttpResponseRedirect(reverse("listing", args=(bid_listing.id,)))
    # Form is invalid.
    messages.add_message(request, messages.WARNING,
                         "We were unable to process your entry.")
    # On error, return the dict needed for listing page and
    # the bound form with invalid data.
    list_args = {"comment_form": None,
                 "bid_form": form,
                 "listing_id": request.POST["listing_id"],
                 "user_id": request.user.id}
    return render(request, "auctions/listing.html",
                  _get_listing_dict(list_args))


def listing(request, listing_id):
    list_args = {"comment_form": None,
                 "bid_form": None,
                 "listing_id": listing_id,
                 "user_id": request.user.id}
    return render(request, "auctions/listing.html",
                  _get_listing_dict(list_args))

def checklist(request):
    return render(request, "auctions/checklist.html")

def faqs(request):
    return render(request, "auctions/faqs.html")

def option(request):
    return render(request, "auctions/option.html")

def _get_listing_dict(list_args):
    """
    Prepares data and forms necessary to the Listing page.
    :param list_args: comment_form, bid_form, listing_id, user_id
    :return: dict needed for listing.html
    """
    comment_form = list_args["comment_form"]
    if not comment_form:
        comment_form = CommentForm()

    bid_form = list_args["bid_form"]
    if not bid_form:
        bid_form = BidForm()

    listing_id = list_args["listing_id"]
    user_id = list_args["user_id"]
    user_watchlist = None

    try:
        view_listing = Listing.objects.get(pk=listing_id)
        comments = Comment.objects.get_queryset().filter(listing=view_listing)
        if user_id:
            user_watchlist = User.objects.get(pk=int(user_id)).watchlist.all()
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    except User.DoesNotExist:
        raise Http404("User not found.")
    return {
        "listing": view_listing,
        "form": bid_form,
        "comment_form": comment_form,
        "comments": comments,
        "watchlist": user_watchlist
    }


def all_listings(request):
    listings = Listing.objects.all().order_by('-listing_date')
    user_watchlist = None
    if request.user.is_authenticated:
        user_watchlist = User.objects.get(
            pk=int(request.user.id)).watchlist.all()
    return render(request, "auctions/all_listings.html", {
        "listings": listings,
        "category": Listing.CATEGORY_CHOICES,
        "city": Listing.CITY_CHOICES,
        "watchlist": user_watchlist,
        "category_heading": "All Listings",
        "city_heading": "All Listings"
    })


def category_sort(request, category):
    # Category of "U" gets only listings created by User.
    if category is "U":
        listings = Listing.objects.all().filter(
            owner=request.user.id).order_by('-listing_date')
        heading = "Listings"
    else:
        listings = Listing.objects.all().filter(
            category=category, status=Listing.ACTIVE).order_by('-listing_date')
        heading = models.get_category_label(category)

    return render(request, "auctions/all_listings.html", {
        "listings": listings,
        "category": Listing.CATEGORY_CHOICES,
        "category_heading": heading
    })

def city_sort(request, city):
    if city is "U":
        listings=Listing.objects.all().filter(
            owner=request.user.id).order_by('-listing_date')
        heading = "Listings"
    else:
        listings=Listing.objects.all().filter(
            city=city, status=Listing.ACTIVE).order_by('-listing_date')
        heading=models.get_city_label(city)
    return render(request, "auctions/all_listings.html",{
        "listings":listings,
        "city":Listing.CITY_CHOICES,
        "city_heading":heading
    })
    
@require_http_methods(["POST"])
@login_required(login_url="/login")
def close_listing(request):
    try:
        target_listing = Listing.objects.get(
            pk=int(request.POST["listing_id"]))
        target_listing.status = Listing.CLOSED
        target_listing.save()
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    messages.add_message(request, messages.SUCCESS,
                         "Post has been closed.")
    return HttpResponseRedirect(
        reverse("listing", args=(request.POST["listing_id"],)))


@login_required(login_url="/login")
def create_listing(request):
    form = ListingForm(request.POST)
    form.owner = request.user
    # On POST, create the listing.
    if request.method == "POST":
        if form.is_valid():
            try:
                # Create the Listing object from the form, add the
                # User before saving.
                new_listing = form.save(commit=False)
                new_listing.owner = request.user
                new_listing.save()
            except IntegrityError:
                messages.add_message(request, messages.WARNING,
                                     "We were unable to add the listing.")
                return render(request, "auctions/create_listing.html",
                              {"form": form})
            # Successfully created a Listing
            messages.add_message(request, messages.SUCCESS,
                                 "Success! Your listing has been created.")
            return HttpResponseRedirect(
                reverse("listing", args=(new_listing.id,)))
        # Form is not valid
        messages.add_message(request, messages.WARNING,
                             "Something went wrong. Please try again.")
        return render(request, "auctions/create_listing.html", {"form": form})
    # Default is to render the create_listing form
    else:
        return render(request, "auctions/create_listing.html",
                      {"form": ListingForm()})


@require_http_methods(["POST"])
@login_required(login_url="/login")
def add_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        try:
            target_listing = Listing.objects.get(
                pk=int(request.POST["listing_id"]))
            # Create a Comment object from the form, add Listing
            # and User data before saving.
            new_comment = form.save(commit=False)
            new_comment.listing = target_listing
            new_comment.owner = request.user
            new_comment.save()
        except Listing.DoesNotExist:
            raise Http404("Listing not found.")
        except IntegrityError:
            messages.add_message(
                request,
                messages.WARNING,
                "We were unable to add the comment. "
                + "Please give it another try"
            )
            return HttpResponseRedirect(
                reverse("listing", args=(target_listing.id,)))

        # Comment was successfully created
        messages.add_message(request, messages.SUCCESS,
                             "Success! <a href='#comments'>Your comment</a>"
                             + " has been saved")
        return HttpResponseRedirect(
            reverse("listing", args=(target_listing.id,)))

    # Form is invalid. Message the user and
    # get the dict needed for listing page.
    messages.add_message(request, messages.WARNING,
                         "We were unable to add the comment.")
    messages.add_message(request, messages.WARNING,
                         _process_form_errors(form))
    list_args = {"comment_form": form,
                 "bid_form": None,
                 "listing_id": request.POST["listing_id"],
                 "user_id": request.user.id}
    return render(request, "auctions/listing.html",
                  _get_listing_dict(list_args))


def _process_form_errors(form):
    """
    Formats error messages from a bound form.
    :param form: bound form with errors
    :return: formatted error messages
    """
    error_message = ""
    for field, validation_error in form.errors.as_data().items():
        error_message = error_message + field.title() + ": "
        for warning in validation_error:
            for item in warning:
                error_message = error_message + " " + item + " "
    return error_message


@login_required(login_url="/login")
def watchlist(request, user_id):
    try:
        user_watchlist = User.objects.get(pk=int(user_id)).watchlist.all()
        
    except User.DoesNotExist:
        raise Http404("User not found.")
    return render(request, "auctions/all_listings.html", {
        "listings": user_watchlist,
        "category": Listing.CATEGORY_CHOICES,
        "watchlist_flag": "True",
        "category_heading": "Favorites"
        
    })
    





   


@login_required(login_url="/login")
def add_watchlist(request):
    try:
        user = User.objects.get(pk=int(request.user.id))
        selected_listing = Listing.objects.get(
            pk=int(request.POST["listing_id"])
        )
        user.watchlist.add(selected_listing)
    except User.DoesNotExist:
        raise Http404("User not found.")
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    except IntegrityError:
        return render(request, "auctions/index.html", {
            "message": "Failed when adding to watchlist.",
            "watchlist_flag": "True"
        })
    # Listing was added to watchlist.
    messages.add_message(request, messages.SUCCESS,
                         "Success! The listing has been added. ")
    return HttpResponseRedirect(reverse("watchlist", args=(user.id,)))


@require_http_methods(["POST"])
@login_required(login_url="/login")
def remove_watchlist(request):
    try:
        delete_listing = Listing.objects.get(
            pk=int(request.POST["listing_id"]))
        user = User.objects.get(pk=int(request.user.id))
        user.watchlist.remove(delete_listing)
    except User.DoesNotExist:
        raise Http404("User not found.")
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    except IntegrityError:
        messages.add_message(request, messages.WARNING,
                             "Failed to remove this item from Watchlist. "
                             + "Please try again.")
        return HttpResponseRedirect(
            reverse("listing", args=(delete_listing.id,)))
    # Listing was removed from watchlist
    messages.add_message(request, messages.SUCCESS,
                         "Success. This listing has been removed from your "
                         + "Watchlist.")
    return HttpResponseRedirect(reverse("listing", args=(delete_listing.id,)))


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        # Check if authentication succeeded and login.
        if user is not None:
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Success! You are now logged in.")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(
                request,
                messages.WARNING,
                "We had Login troubles. Please check your username and "
                + "password or register if you haven't already.")
            return render(request, "auctions/login.html")
    # Default is to render the login form
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    messages.add_message(
        request,
        messages.SUCCESS,
        "Success! You've been logged out.")
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                # Attempt to create new user
                # Note: calling form.save does not encode password
                # but user.save does
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])
                user.save()
            except IntegrityError:
                messages.add_message(request, messages.WARNING,
                                     "Username already taken.")
                return render(request, "auctions/register.html")
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "<h4>Well Done!</h4><p>You've successfully registered for "
                + "Auction NOW and are ready to start bidding! Be sure to "
                + "use the <strong>watchlist</strong> feature and we welcome "
                + "your <strong>comments</strong> on listings. </p > ")
            return HttpResponseRedirect(reverse("index"))
        else:
            # Form is not valid.
            messages.add_message(request, messages.WARNING,
                                 "<p><strong>Something went "
                                 + "wrong:</strong></p>")
            return render(request, "auctions/register.html", {"form": form})
    # Default (GET request) is to render the register user form.
    else:
        return render(request, "auctions/register.html",
                      {"form": RegisterForm()})
def res(request):
    q=Article_list.objects.all()
    q.delete()
    article_l=[]
    category_var=request.GET['category']
    num_recomm_var=int(request.GET['num_recomm'])

    print(os.getcwd())
    ds=pd.read_csv('test_case.csv')
    
            
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,1), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['Link'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    results={}

    for category, row in ds.iterrows():
        similar_indices = cosine_similarities[category].argsort()[:-40:-1]
        similar_items = [(cosine_similarities[category][i], ds['Category'][i]) for i in similar_indices]
        
        results[row['Category']]=similar_items[1:]

    print('done!')

    def item(category):
        return ds.loc[ds['Category'] == category]['Link'].tolist()[0]
        
        
        #.split('-')
    
    def recommend(category,num):
        #print("Recommending Articles")
        recs = results[category][:num]

        for rec in recs:
            #print("Recommended articles will be found on your home page! Hope you find them useful")
            article_l.append(item(rec[1]))
            t=Article_list(link=item(rec[1]),cos_sim=float(rec[0]))
            t.save()
    recommend(category_var,num_recomm_var)
    a={'category':article_l}
    print('Over')
    print(article_l)

    article=Article_list.objects.all()
    print(article)

    return render(request,'auctions/res.html',{'article_dict':article})







