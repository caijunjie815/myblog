from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView

from blog.models import Post, Category, Comments
from .forms import CommentForm


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

    def get_queryset(self):  # get queryset
        return Post.objects.filter(category=self.kwargs['category']).order_by(
            '-id')  # use passed category id to obtain posts.

    def get_context_data(self, **kwargs):  # pass extra arguments to template.
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category'])
        context['category'] = category.name  # the variable name "category" will be used in template in {{category}}.
        return context


class PostView(DetailView):  # view an article's all content.
    model = Post
    template_name = 'article.html'

    # define comment function
    def comment_sort(self, comments):  # sort comments which will be display in template.
        self.comment_list = []  # the final list of comments
        self.top_level = []  # save top comments in a list
        self.sub_level = {}  # save kid comments in a dict.
        # classify comments into top comment list or kid comment dictionary.
        for comment in comments:
            if comment.reply == None:
                self.top_level.append(comment)
            else:
                self.sub_level.setdefault(comment.reply.id, []).append(comment)  # key=parent's id, value= this comment.
        for top_comment in self.top_level:
            self.format_show(top_comment)  # call a recursive function
        return self.comment_list  # return sorted list of comments.

    def format_show(self, comment):  # recursive function to save comment, followed by its kid comment.
        self.comment_list.append(comment)
        try:
            self.kids = self.sub_level[comment.id]  # obtain all replay in a comment.
        except KeyError:  # if no replay
            pass  # end recursive
        else:
            for kid in self.kids:
                self.format_show(kid)  # next recursive

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # list comments
        comments = Comments.objects.filter(article=self.kwargs['pk'])  # query comments by post id.
        context['comment_list'] = self.comment_sort(comments)

        # pass comment form to template
        comment_form = CommentForm()
        context['comment_form'] = comment_form

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


class PostForm(FormView):
    def post_comment(self, request):
        if request.method == 'POST':  # if a post request
            comment = Comments()  # create a instance of Comments class
            comment.article = Post.objects.get(id=request.POST.get('article'))  # get article id
            if request.POST.get('reply') != '0':  # if not reply to the article
                comment.reply = Comments.objects.get(id=request.POST.get('reply'))  # get reply objective
            form = CommentForm(request.POST, instance=comment)
            # combine input form data and the instance to create a whole CommentForm instance
            if form.is_valid():  # check form is valid
                try:
                    form.save()  # save posted form date into database
                    result = 'Successfully comment!'
                except:
                    result = 'AN EXCEPTION OCCURS!'
            else:  # if form is not valid
                result = 'FORM IS NOT VALID!'
            return result
        else:
            pass
