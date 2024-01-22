from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Followers(models.Model):
    # User = Standard Django User
    # user = User
    followed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followed_by"
    )
    
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    # To return text representation of the Object
    def __str__(self):
        return f"{ self.followed_by.id} is following { self.following.id }"
    
    # Create a unique index
    class Meta:
        unique_together = ('followed_by','following')