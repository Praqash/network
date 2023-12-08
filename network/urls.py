from django.urls import path
from . import views
from . views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


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
    path("profile/<str:username>", views.profile, name = "profile"),
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/show_profile_picture/', views.show_profile_picture, name='show_profile_picture'),
    
]
