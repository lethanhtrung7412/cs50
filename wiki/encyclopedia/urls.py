from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_entry_page, name="entry"),
    path("new_entry", views.new_entry, name='new_entry'),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit_entry"),
    path("random", views.random_entry, name="random_entry")
]
