from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import UserCreationForm1, PostForm, UserUpdateForm, ProfileUpdateForm
from .models import Post, Profile, Comment, get_guest_user

TOPICS = ["Politics", "Technology", "Daily", "Default"]


def post_list_view(request, filter_by_author=False):
    selected_topics = request.GET.getlist("topics")
    if not selected_topics:
        # If not in request at all, means haven't checkbox yet, all selected
        selected_topics = TOPICS
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(topic__in=selected_topics)

    if filter_by_author and request.user.is_authenticated:
        posts = posts.filter(author=request.user)

    posts = posts.order_by("-date_posted")
    comments = Comment.objects.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "topics": TOPICS,
        "selected_topics": selected_topics,
        "page_obj": page_obj,
        "filter_by_author": filter_by_author,
        "comments": comments,
    }
    return render(request, "app/home.html", context)


def home(request):
    return post_list_view(request)


def my_post(request):
    return post_list_view(request, filter_by_author=True)


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


def signin(request):
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
        return render(request, "app/signin.html", {"form": form})


def signout(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    # for old user, which was created before profile function
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "app/profile.html", context)


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


def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("comment")
        if content:
            if request.user.is_authenticated:
                user = request.user
            else:
                user = get_guest_user()
            Comment.objects.create(post=post, author=user, content=content)
    return redirect("home")
