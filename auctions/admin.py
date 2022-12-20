from django.contrib import admin

from .models import Listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display=("id", "title", "description", "bid", "image", "category", "timestamp")



admin.site.register(Listing, ListingAdmin)