from django.urls import path

from blog import views as blog_views
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('category/<int:category>', CategoryList.as_view(), name='category'),
    # name is mapping this url, which can be used in templates
    # <int:category> is the keywords matching self.kwargs['category'] in views.py
    path('search/', Search.as_view(), name='search'),
    path('article/<int:pk>/', PostView.as_view(), name='article'),
    path('article/<int:article_id>/comment/', blog_views.post_comment, name='comment'),
    path('about/', blog_views.about, name='about'),
]
