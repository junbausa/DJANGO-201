from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.models import User
from feed.models import Post

# Create your views here.
class ProfileDetailView(DetailView):
    
    http_method_names = ['get']     # Default method = get
    template_name = 'profiles/detail.html'

    model = User # from django.contrib.auth.models
    context_object_name = "user"

    slug_field = "username"
    # from urls.py urlpatterns
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):

        # user = username (slug field / slug url)
        user = self.get_object()

        context = super().get_context_data(**kwargs)
        context["total_posts"] = Post.objects.filter(author = user ).count()
        # TODO Add total followers
        return context
    

