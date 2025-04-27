from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class Post(models.Model):
    TOPICS = [
        ("Politics", "Politics"),
        ("Technology", "Technology"),
        ("Daily", "Daily"),
        ("Default", "Default"),
    ]
    title = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=20, choices=TOPICS, default="Default")
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_img")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        length = 80
        if img.height > length or img.width > length:
            output_size = (length, length)
            img.thumbnail(output_size)
            img.save(self.image.path)


def get_guest_user():
    return User.objects.get(username="guest")  # manually created


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.SET(get_guest_user), default=get_guest_user
    )
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment of {self.post.title}"


# from django.contrib.auth.models import AbstractUser
# class User(AbstractUser):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)

#     avatar = models.ImageField(null=True, default="avatar.svg")

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
