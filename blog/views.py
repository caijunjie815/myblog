from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from blog.models import Post, Category, Comments
from .forms import CommentForm


# Create your views here.
class PostList(ListView):
    """
    list view for index.html
    """
    model = Post
    template_name = 'index.html'
    queryset = Post.objects.all().order_by('-id')
    paginate_by = 5  # set numbers of posts per page.


class CategoryList(ListView):
    """
    list all posts in a given category ordered by posted time.
    """
    model = Post
    template_name = 'category.html'
    paginate_by = 5

    def get_queryset(self):  # get queryset
        return Post.objects.filter(category=self.kwargs['category']).order_by('-id')

    def get_context_data(self, **kwargs):  # pass extra arguments to template.
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category'])
        context['category'] = category.name  # the variable name "category" will be used in template in {{category}}.
        return context


class PostView(DetailView):
    """
    display an article's detail.
    """
    model = Post
    template_name = 'article.html'

    # inheritance Class DetailView and extend to define new attributes
    def __init__(self):
        self.comment_list = []  # the final list of comments
        self.top_level = []  # save top comments in a list
        self.sub_level = {}
        super().__init__()

    # define comment function
    def comment_sort(self, comments):
        """
        sort comments in a parent-kid recursive structure.
        :param comments: all comments belong to an article
        :return: sorted comment list of an article

        """
        """
        for comment in comments:
            if comment.reply is None:
                self.top_level.append(comment)
            else:
                self.sub_level.setdefault(comment.reply.id, []).append(comment)  # key=parent's id, value= kid comment.
        """
        # use list generate expression to place instead of codes in block quotes above.
        [self.top_level.append(comment) for comment in comments if comment.reply is None]
        [self.sub_level.setdefault(comment.reply.id, []).append(comment) for comment in comments if comment.reply]
        [self.format_show(top_comment) for top_comment in self.top_level]  # call a recursive function
        return self.comment_list  # return sorted list of comments.

    def format_show(self, comment):
        """
        :param comment: a parent comment
        :return: the list of parent comment and its kid comments
        """
        self.comment_list.append(comment)
        try:
            kids = self.sub_level[comment.id]  # obtain all replay belongs to a comment.
        except KeyError:  # if no replay
            return self.comment_list  # end recursive
        else:
            [self.format_show(kid) for kid in kids]  # next recursive

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get session and save into context.
        try:
            context['session'] = {
                'name': self.request.session['name'],
                'email': self.request.session['email'],
                'content': self.request.session['content']
            }
        except Exception:  # do nothing if has exception
            pass

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


@require_POST  # only accept a POST request; otherwise return a  django.http.HttpResponseNotAllowed
def post_comment(request):
    """
    function to handle post request from comment form.
    if valid form, save form data into database and return a redirected page.
    if not, return previous page.

    :param request: http POST request
    :return: redirected page if valid; otherwise, previous page with prompt message
    """
    # session input to auto-fill
    request.session['name'] = request.POST.get('name')
    request.session['email'] = request.POST.get('email')

    comment = Comments()  # create a instance of Comments class
    article_id = request.POST.get('article')  # get article id

    comment.article = Post.objects.get(id=article_id)
    if request.POST.get('reply') != '0':  # if reply to a comment
        comment.reply = Comments.objects.get(id=request.POST.get('reply'))  # get reply objective
    form = CommentForm(request.POST, instance=comment)
    # combine input form data and the instance to create a whole CommentForm instance
    if form.is_valid():  # if form is not valid
        try:
            form.save()  # save posted form date into database
            request.session['content'] = ''  # save null into session if successful
            messages.success(request, 'Your comment was added successfully!')
            return redirect('blog:article', pk=article_id)
        except Exception:
            request.session['content'] = request.POST.get('content')  # save input content in session if fail
            messages.warning(request, 'AN EXCEPTION OCCURS!')
    messages.error(request, 'Please correct your error above!')  # if not a valid form


class NavList(ListView):  # list category names in navigation bar
    model = Category
    template_name = 'nav.html'
