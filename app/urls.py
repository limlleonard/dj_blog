from django.urls import include, path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("my_post", views.my_post, name="my-post"),
    path("register/", views.register, name="register"),
    # path("signin/", views.signin, name="signin"),
    path("profile/", views.profile, name="profile"),
    path("signout/", views.signout, name="signout"),
    # path("newpost/", views.newpost, name="newpost"),
    path(
        "signin/",
        LoginView.as_view(template_name="app/signin.html", next_page="home"),
        name="signin",
    ),
    path("post/new/", views.post_create_update, name="post-create"),
    path("post/<int:pk>/edit/", views.post_create_update, name="post-update"),
    path("post/<int:pk>/delete/", views.post_delete, name="post-delete"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add-comment"),
]
