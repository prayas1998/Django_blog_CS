import os.path

from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    # Overriding the save method:
    # def save(self, *args, **kwargs):
    #     # Check if the profile already exists to get the old image
    #     if self.pk:  # Check if this is not a new instance
    #         old_image = Profile.objects.get(user_id=self.user.id).image
    #         # If the old image is not the default image
    #         if old_image and old_image.name != 'default.jpg':
    #             # If the old image exists and is not the current image
    #             if os.path.exists(old_image.path) and self.image != old_image:
    #                 os.remove(old_image.path)  # Delete the old image
    #
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
