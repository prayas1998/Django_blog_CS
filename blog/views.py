from django.shortcuts import render, redirect
from django.http import HttpResponse

from blog.forms import PostForm
from blog.models import Post
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)


# Creating a class-based view similar to 'home' function based view above.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<ViewType>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # To show latest blogs on top


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  # Returns an 'HttpResponseRedirect'


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
