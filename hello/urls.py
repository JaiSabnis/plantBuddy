from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.myprofile, name="myprofile"),
    path("profiles/<int:user_id>", views.profile, name="profile"),   
    path("<int:user_id>/accept", views.accept, name="accept"),
    path("new-plant", views.newPlant, name="newPlant"),
    path("plants/<int:plant_id>", views.plantDisplay, name="plantDisplay" ),
    path("plants/discussions/<int:post_id>", views.postDisplay, name="postDisplay"),
    path("plants/<int:plant_id>/new-discussion", views.newPost, name="newPost" ),


]
