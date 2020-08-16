
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost",views.new_post, name="newpost"),

    # API routes
    path("posts/<int:page_num>", views.all_posts, name="all_posts"),
    path("posts/<int:user_id>/<int:page_num>", views.all_posts, name="user_posts"),
    path("posts/<str:user_id>/<int:page_num>", views.all_posts, name="follow_posts"),
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("profile/<int:id>", views.load_profile, name="profile"),
    path("like/<int:id>", views.like_post, name="like"),
    path("follow/<int:user_id>", views.follow, name="follow")
]
