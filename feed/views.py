# Create your views here.

from django.views.generic import ListView, DetailView, CreateView
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

class PostDetailView(DetailView):
    
    # new options for django201
    http_method_names = ['get']     # Default method = get
    template_name = 'feed/detail.html'

    model = Post
    context_object_name = "post" # this refers to context object default is "object"

 # new options for django201. in django101, we used FormView
class CreateNewPost(CreateView):
    
    template_name ='feed/create.html'
    model = Post 

    # Fields you want to include in form...
    fields = ['text']