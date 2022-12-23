from django.contrib import admin

from .models import Listing, Watchlist, Bid

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display=("id", "title", "description", "bid", "image", "category", "timestamp")

class BidAdmin(admin.ModelAdmin):
    list_display=("user", "listing", "bid", "isCurrent")



admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist)
admin.site.register(Bid, BidAdmin)