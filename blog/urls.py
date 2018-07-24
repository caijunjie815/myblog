from django.urls import path

from blog import views as blog_views
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('category/<int:category>', CategoryList.as_view(), name='category'),
    path('search/', Search.as_view(), name='search'),
    path('article/<int:pk>/', PostView.as_view(), name='article'),
    path('article/<int:article_id>/comment/', blog_views.post_comment, name='comment'),
    path('about/', blog_views.about, name='about'),
]
