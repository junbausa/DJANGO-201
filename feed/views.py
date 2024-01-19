# Create your views here.

from django.views.generic import ListView, DetailView, CreateView
# ccbv.co.uk for django views documentation

# models here
from .models import Post

# this will check if user is logged in or not. For Tasks that has database updates
from django.contrib.auth.mixins import LoginRequiredMixin

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
class CreateNewPost(LoginRequiredMixin,CreateView):
    
    template_name ='feed/create.html'
    model = Post 

    # Fields you want to include in form...
    fields = ['text']

    # CreateViews require success URLS
    success_url='/'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        # Grab form but no save
        obj = form.save(commit = False)
        obj.author = self.request.user

        obj.save()

        return super().form_valid(form)
    
    
    