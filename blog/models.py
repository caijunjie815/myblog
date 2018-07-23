from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, unique=True)
    content = RichTextField(config_name='mycfg')
    posted_time = models.DateField('date posted', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nickname', max_length=20)
    email = models.EmailField()
    content = models.TextField()
    posted_time = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.content
