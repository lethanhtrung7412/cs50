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

class Category(TimeStampedModel):
    name = models.CharField()

class Listing(TimeStampedModel):
    product_name = models.CharField()
    img = models.URLField()
    bid_price = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories", blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

class Bidding(TimeStampedModel):
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    bidder_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item_bidding = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(TimeStampedModel):
    content = models.TextField()
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
