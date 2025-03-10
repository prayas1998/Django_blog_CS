from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    db_health_check,
    post_count,
)

# urlpatterns = [
#     path('', views.home, name='blog-home'),  # Imported the home function from 'views'
#     path('about/', views.about, name='blog-about'),
# ]


urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("about/", views.about, name="blog-about"),
    #! urls for cronjobs:
    path("db-health-check/", views.db_health_check, name="db_health_check"),
    path("post-count/", views.post_count, name="post-count"),
]
