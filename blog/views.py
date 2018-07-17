from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post, Category, Comments


# Create your views here.
class PostList(ListView):  # index.html: list all posts ordered by posted time.
    model = Post
    template_name = 'index.html'
    queryset = Post.objects.all().order_by('-id')
    paginate_by = 5  # set numbers of posts per page.


class CategoryList(ListView):  # category.html :list all posts in a given category ordered by posted time.
    model = Post
    template_name = 'category.html'
    paginate_by = 5

    def get_queryset(self):  # define queryset method
        return Post.objects.filter(category=self.kwargs['category']).order_by(
            '-id')  # use passed category id to obtain posts.

    def get_context_data(self, **kwargs):  # pass extra args to template.
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category'])
        context['category'] = category.name  # the variable name "category" will be used in template in {{category}}.
        return context


class PostView(DetailView):  # view an article's all content.
    model = Post
    template_name = 'article.html'

    # define comment function
    def comment_sort(self, comments):  # 评论排序函数
        self.comment_list = []  # 排序后的评论列表
        self.top_level = []  # 存储顶级评论
        self.sub_level = {}  # 存储回复评论
        for comment in comments:  # 遍历所有评论
            if comment.reply == None:  # 如果没有回复目标
                self.top_level.append(comment)  # 存入顶级评论列表
            else:  # 否则
                self.sub_level.setdefault(comment.reply.id, []).append(comment)  # 以回复目标（父级评论）id为键存入字典
        for top_comment in self.top_level:  # 遍历顶级评论
            self.format_show(top_comment)  # 通过递归函数进行评论归类
        return self.comment_list  # 返回最终的评论列表

    def format_show(self, top_comment):  # 递归函数
        self.comment_list.append(top_comment)  # 将参数评论存入列表
        try:
            self.kids = self.sub_level[top_comment.id]  # 获取参数评论的所有回复评论
        except KeyError:  # 如果不存在回复评论
            pass  # 结束递归
        else:  # 否则
            for kid in self.kids:  # 遍历回复评论
                self.format_show(kid)  # 进行下一层递归

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comments.objects.filter(article=self.kwargs['pk'])  # query comments by post id.
        context['comment_list'] = self.comment_sort(comments)
        return context


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
