from django.urls import include, path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("my_post", views.my_post, name="my-post"),
    path("register/", views.register, name="register"),
    # path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("signout/", views.signout, name="signout"),
    # path("newpost/", views.newpost, name="newpost"),
    path(
        "signup/",
        LoginView.as_view(template_name="app/signup.html", next_page="home"),
        name="signup",
    ),
    path("post/new/", views.post_create_update, name="post-create"),
    path("post/<int:pk>/edit/", views.post_create_update, name="post-update"),
    path("post/<int:pk>/delete/", views.post_delete, name="post-delete"),
]
