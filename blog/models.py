from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=0)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    posted_time = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Comments(models.Model):
    name = models.CharField('Nickname', max_length=20, default=0)
    email = models.EmailField(default=0)
    content = models.TextField()
    posted_time = models.DateField(auto_now=True)
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.content
