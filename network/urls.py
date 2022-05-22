from django.urls import path
from . import views
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("com", views.com, name="com"),
    path("like", views.like, name = "like"),
    path("update", views.update, name = "update"),
    path("trash", views.trash, name = "trash"),
    path("follow", views.follow, name = "follow"),
    path("profile/<str:username>", views.profile, name = "profile")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)