from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class TimeStampedModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Listing(TimeStampedModel):
    product_name = models.CharField()
    img = models.URLField()
    bid_price = models.FloatField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

class Bidding(TimeStampedModel):
    amount = models.FloatField()
    bidder_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item_bidding = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(TimeStampedModel):
    content = models.TextField()
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")