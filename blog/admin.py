from django.contrib import admin

from blog.models import *


# Register your models here.

@admin.register(Post)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'posted_time')


@admin.register(Comments)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("article", 'name', 'posted_time', 'content', 'reply')


admin.site.register((Category, Tag))
