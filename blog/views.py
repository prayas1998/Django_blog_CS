from django.shortcuts import render
from django.http import HttpResponse

from blog.models import Post
from django.views.generic import ListView, DetailView


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


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
