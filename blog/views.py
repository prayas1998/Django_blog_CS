from django.shortcuts import render
from django.http import HttpResponse

from blog.models import Post


# posts = [
#     {
#         'author': 'User1',
#         'title': 'Blog Post 1',
#         'content': 'First blog post',
#         'date_posted': '30 july 2024'
#     },
#     {
#         'author': 'User2',
#         'title': 'Blog Post 2',
#         'content': 'Second blog post',
#         'date_posted': '30 july 2024'
#     },
# ]


def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
