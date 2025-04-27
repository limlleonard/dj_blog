from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Profile

# from .models import Room, User


class UserCreationForm1(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "topic"]


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["username"]


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


# class RoomForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = '__all__'
#         exclude = ['host', 'participants']


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['avatar', 'name', 'username', 'email', 'bio']
