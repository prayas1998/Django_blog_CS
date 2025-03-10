from django.db.models.signals import post_save
from django.contrib.auth.models import User  # Sender of signal
from django.dispatch import receiver  # receiver of signal
from .models import Profile


@receiver(
    post_save, sender=User
)  # When user is saved send this signal. This signal is received triggers create_profile signal
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
