import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, PostForm


@login_required(login_url="login")
def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            form.save_m2m()
            return render(request, "network/index.html")
        else:
            return render(request, "network/new_post.html", {
                "form": form
            })
    return render(request, "network/new_post.html", {
        "form": PostForm
    })

def all_posts(request, page_num, user_id=None):
    user = request.user
    if user_id is None:
        posts = Post.objects.order_by("-timestamp").all()
    elif user_id == "following":
        posts = Post.objects.filter(author__in = user.following.all()).order_by("-timestamp").all()
    else:
        posts = Post.objects.filter(author=User.objects.get(pk=user_id)).order_by("-timestamp").all()
    p = Paginator(posts, 10)
    lst = []
    for post in p.page(page_num).object_list:
        lst_c = []
        if post in user.liked_post.all():
            lst_c.extend([post.serialize(), "Unlike"])
        else:
            lst_c.extend([post.serialize(), "Like"])
        if user.id == post.serialize()["author_id"]:
            lst_c.extend([True])
        else:
            lst_c.extend([False])
        lst.append(lst_c)
    return JsonResponse([lst,p.num_pages], safe=False)


@login_required(login_url="login")
def load_profile(request, id):
    u = User.objects.get(pk=id)
    user = request.user
    flag = False
    follow = "Follow"
    if user != u:
        flag = True
        if u in user.following.all():
            follow = "Unfollow"
    return JsonResponse([u.serialize(), flag, follow], safe=False)

@csrf_exempt
def like_post(request, id):
    if request.method == "PUT":
        p = Post.objects.get(pk=id)
        u = request.user
        like_status = "Like"
        if p in u.liked_post.all():
            u.liked_post.remove(p)
            p.likes = p.likes - 1
        else:
            u.liked_post.add(p)
            like_status = "Unlike"
            p.likes = p.likes + 1
        p.save()
        return JsonResponse(like_status, safe=False)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
def follow(request, user_id):
    if request.method == "PUT":
        u = User.objects.get(pk=user_id)
        user = request.user
        follow_status = "Follow"
        if user != u:
            if u in user.following.all():
                user.following.remove(u)
            else:
                user.following.add(u)
                follow_status = "Unfollow"
            user.save()
            return JsonResponse(follow_status, safe=False)
        else:
            return JsonResponse(status=403)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
def edit_post(request, post_id):
    if request.method == "PUT":
        user = request.user
        post = Post.objects.get(pk=post_id)
        if user == post.author:
            data = json.loads(request.body)
            post.body = data.get("text")
            post.save()
            return JsonResponse({"message": "Edit succesfull"},status=203)
        else:
            return JsonResponse(status=403)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
