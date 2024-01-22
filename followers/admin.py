from django.contrib import admin
from .models import Followers

# Register your models here.
class FollowerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Followers,FollowerAdmin) 