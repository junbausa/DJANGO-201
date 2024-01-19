from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    # User = Standard Django User
    # user = User
    user = models.OneToOneField(
                User,
                on_delete=models.CASCADE,
                related_name="profile"
            )
    
    def __str__(self):
        return self.user.username
    
# Signal / Same as callback in Javascript
# It's like an add in
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a new Profile object when a Django User is created"""
    if created:
        Profile.objects.create(user=instance)
