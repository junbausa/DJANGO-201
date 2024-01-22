from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.models import User

# Create your views here.
class ProfileDetailView(DetailView):
    
    http_method_names = ['get']     # Default method = get
    template_name = 'profile/profile.html'

    model = User # from django.contrib.auth.models
    context_object_name = "user"

    slug_field = "username"
    # from urls.py urlpatterns
    slug_url_kwarg = "username"


