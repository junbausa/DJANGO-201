# Create your views here.

from django.views.generic import ListView
# ccbv.co.uk for django views documentation

# models here
from .models import Post

class HomeView(ListView):
    template_name = 'feed/homepage.html'
    model = Post

    # new options for django201
    http_method_names = ['get']     # Default method = get
    context_object_name = "posts" # this refers to context object default is "object"
    
    queryset = Post.objects.all().order_by('-id')[0:30]
