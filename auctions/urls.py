from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/addWatchlist", views.addWatchlist, name="addWatchlist"),
    path("<int:listing_id>/removeWatchlist", views.removeWatchlist, name="removeWatchlist"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/win", views.win, name="win"),
    path("<int:listing_id>/comment", views.comment, name="comment"),

    
]
