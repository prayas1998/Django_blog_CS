from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from django.http import HttpResponse, JsonResponse
from django.db import connection

from blog.forms import PostForm
from blog.models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from helper import check_profanity


def home(request):
    context = {"posts": Post.objects.all(), "title": "Home"}
    return render(request, "blog/home.html", context)


# Creating a class-based view similar to 'home' function based view above.
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"  # <app>/<model>_<ViewType>.html
    context_object_name = "posts"
    ordering = ["-date_posted"]  # To show latest blogs on top
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"  # <app>/<model>_<ViewType>.html
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post


# When using class-based views, you can achieve the same behavior as with login_required by using the LoginRequiredMixin.
# This mixin should be at the leftmost position in the inheritance list.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    # template_name = 'blog/post_form.html'  # <app_name>/<ModelMame>_form.html

    def form_valid(self, form):
        # Grab 'title' and 'content' from cleaned_data
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        if check_profanity(title) or check_profanity(content):
            messages.error(
                self.request,
                "Your post contains inappropriate content. Please revise and try again.",
                extra_tags="danger",
            )
            return self.form_invalid(form)

        form.instance.author = self.request.user
        return super().form_valid(form)  # Returns an 'HttpResponseRedirect'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        # Grab 'title' and 'content' from cleaned_data
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        if check_profanity(title) or check_profanity(content):
            messages.error(
                self.request,
                "Your post contains inappropriate content. Please revise and try again.",
                extra_tags="danger",
            )
            return self.form_invalid(form)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  # For UserPassesTestMixin (Refer Docs)
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # User is logged in but doesn't have permission
            messages.error(
                self.request,
                f"You don't have permission to update this post. You can only update the posts created by you!",
                extra_tags="danger",
            )
            return redirect("blog-home")
        else:
            # User is not logged in
            return super().handle_no_permission()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):  # For UserPassesTestMixin (Refer Docs)
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})


# Note: Endpoints to create cronjobs to keep application active


def db_health_check(request):

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        return HttpResponse(f"Database is active: {result[0]}", status=200)

    except Exception as e:
        return HttpResponse(f"Database connection error: {str(e)}", status=500)


def post_count(request):
    """
    Endpoint that returns the total number of posts in the database.
    """
    try:
        total_posts = Post.objects.count()
        return JsonResponse({"total_posts": total_posts})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
