from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    bid = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.URLField(max_length=255, blank=True)
    category = models.CharField(max_length=255, default="General")
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=True)
    isActive = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won", null=True)
    

    def __str__(self):
        return f"{self.title}| {self.bid}| {self.category}| {self.user}| {self.isActive}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"{self.user} -Watchlisted-> {self.listing}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=5, decimal_places=2)
    isCurrent = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}| {self.listing}| {self.bid}| {self.isCurrent}"




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComments")	
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingComments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.user}| {self.listing}| {self.comment}"