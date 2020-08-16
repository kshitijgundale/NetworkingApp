from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django import forms


class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="follower", blank=True, symmetrical=False)
    liked_post = models.ManyToManyField("Post", related_name="liked_by", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.username,
            "num_following": len(self.following.all()),
            "num_followers": len(self.follower.all()),
        }

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(max_length=512, blank=False)
    likes = models.IntegerField(blank=True, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "post_id": self.id,
            "author_id": self.author.id,
            "author_name": self.author.username,
            "body": self.body,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p")
        }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder':'Compose your post here...', 'rows':3})
        }
        labels = {
            'body': ''
        }


