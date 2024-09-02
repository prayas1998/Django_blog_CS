from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(
        default=timezone.now)  # Default will update the time automatically when a post is created.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # Redirect will redirect you to a specific route.
    # Reverse will return the full URL to that route as a String.
    # In this case we simply want to return the URL as a String and let the view handle the redirect for us.

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
