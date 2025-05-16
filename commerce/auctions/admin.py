from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Listing)
admin.site.register(models.Comment)
admin.site.register(models.Bidding)
admin.site.register(models.Category)