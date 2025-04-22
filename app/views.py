from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import UserCreationForm1, PostForm
from .models import Post

TOPICS = ["Politics", "Technology", "Daily", "Default"]


def home(request):
    if "topics" not in request.GET:
        selected_topics = TOPICS
    else:
        selected_topics = request.GET.getlist("topics")
    posts = Post.objects.filter(topic__in=selected_topics).order_by("-date_posted")

    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "topics": TOPICS,
        "page_obj": page_obj,
        "selected_topics": selected_topics,
    }

    return render(request, "app/home.html", context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm1(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm1()
    return render(request, "app/register.html", {"form": form})


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username OR password does not exit")
    else:
        form = UserCreationForm1()  # userloginform
        return render(request, "app/signup.html", {"form": form})


def signout(request):
    logout(request)
    return redirect("home")


def profile(request):
    return render(request, "app/profile.html")


def newpost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to database yet
            post.author = request.user  # Assign the logged-in user
            post.save()  # Now save to database
            return redirect("home")  # Redirect after POST
    else:
        form = PostForm()
    return render(request, "app/newpost.html", {"form": form})


# views.py


@login_required
def post_create_update(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return HttpResponseForbidden("You are not allowed to edit this post.")
    else:
        post = None

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("home")
    else:
        form = PostForm(instance=post)
    context = {"topics": TOPICS, "selected_topics": TOPICS, "form": form}

    return render(request, "app/post_form.html", context)


# views.py
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect(request.META.get("HTTP_REFERER", "home"))

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("home")  # redirect after deletion
    return render(request, "post_confirm_delete.html", {"post": post})
