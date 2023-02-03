from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =   [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("item/<int:listing_id>", views.listing, name="listing"),
    path("category/<slug:category>/", views.display_category, name="display_category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_id>", views.add_to_watchlist, name = "add_to_watchlist"),
    path("watchlist/remove/<int:listing_id>", views.remove_from_watchlist, name = "remove_from_watchlist"),
    path("placebid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("closebid/<int:listing_id>", views.closebid, name="closebid"),
    path("add_comment/<int:listing_id>", views.comment, name= "add_comment")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)