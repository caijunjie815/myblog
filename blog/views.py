from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Comments, Tag
from django.views.generic import ListView, DetailView
from django.db.models import Q


# Create your views here.
class PostList(ListView):  # index.html: list all posts ordered by posted time.
    model = Post
    template_name = 'index.html'
    queryset = Post.objects.all().order_by('-id')
    paginate_by = 5  # set numbers of posts per page.


class CategoryList(ListView):  # category.html :list all posts in a certain category ordered by posted time.
    model = Category
    template_name = 'category.html'
    paginate_by = 5

    def get_queryset(self):  # define queryset method
        return Post.objects.filter(category=self.kwargs['category']).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category'])
        context['category'] = category.name
        return context


class PostView(DetailView):  # view an article's all content.
    model = Post
    template_name = 'article.html'

    # define comment function
    def get_comment(self, comments):
        pass


class Search(ListView):
    model = Post
    template_name = 'search.html'
    paginate_by = 5

    def get_queryset(self):
        key = self.request.GET['key']
        if key:
            return Post.objects.filter(Q(title__icontains=key) | Q(content__icontains=key)).order_by('-id')
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['key'] = self.request.GET['key']
        return context


def about(request):
    return render(request, 'about.html')
