from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),  # Imported the home function from 'views'
    path('about/', views.about, name='blog-about'),
]
