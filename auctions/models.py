from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owners")
    item_name = models.CharField(max_length=64)
    item_price = models.IntegerField()
    item_image = models.URLField(default=None, blank=True, null=True,)
    item_category = models.CharField(max_length=64, default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.item_name}"

class Listing(models.Model):
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listers", default=None)
    listed_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="listed_items")
    description = models.TextField(default=None, blank=True, null=True,)
    floor_price = models.IntegerField()
    listed_time = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    bidded_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bidded_items")
    bidded_price = models.IntegerField()

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
    commented_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="commented_items")
    comment = models.TextField()

class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchers")
    watched_list = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched_lists")

class Vser(models.Model):
    name = models.CharField(max_length=64, default=None)
    dob = models.DateField()