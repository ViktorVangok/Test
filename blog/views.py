from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from blog.models import Post, Comment
from .forms import CommentForm

from multiprocessing import Process
import logging
import configparser

config = configparser.ConfigParser()
config.read('cnf.ini')
logging.basicConfig(
level=config['LOGGING']['level'],
filename=config['LOGGING']['filename']
)
log = logging.getLogger(__name__)


class HomeView(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/home.html"


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs.get("slug")).select_related('category')


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        p = Process(target=log.info(f'work in {self.context_object_name} , {self.slug_url_kwarg}'))
        return context


class CreateComment(CreateView):
    model = Comment
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()
