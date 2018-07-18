from django.contrib import admin

from blog.models import *


# Register your models here.

@admin.register(Post)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted_time')


@admin.register(Comments)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', "article", 'posted_time', 'content')


admin.site.register((Category, Tag))
