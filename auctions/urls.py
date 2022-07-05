from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("item_detail/<int:element_id>", views.item_detail, name="item_detail"),
    path("item_detail/<int:element_id>/<error_message>", views.item_detail, name="item_detail"),
    path("bidding", views.bidding, name="bidding"),
    path("close_bidding", views.close_bidding, name="close_bidding"),
    path("commenting", views.commenting, name="commenting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category_detail/<str:category>", views.category_detail, name="category_detail"),
]