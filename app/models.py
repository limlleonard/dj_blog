from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)

#     avatar = models.ImageField(null=True, default="avatar.svg")

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


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
