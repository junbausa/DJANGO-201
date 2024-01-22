# Create your views here.

from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
# ccbv.co.uk for django views documentation

# models here
from  followers.models import Follower
from .models import Post

# this will check if user is logged in or not. For Tasks that has database updates
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render

# class HomeView(ListView):
class HomeView(TemplateView):
    template_name = 'feed/homepage.html'
    model = Post

    # new options for django201
    http_method_names = ['get']     # Default method = get
    # context_object_name = "posts" # this refers to context object default is "object"
    
    # queryset = Post.objects.all().order_by('-id')[0:30]
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            # people i follow....
            following = list(
                Follower.objects.filter(followed_by = self.request.user).values_list('following',flat=True)
            )
            if following:
            # Filter request by author...
                posts = Post.objects.filter(author__in=following)
            else:
                posts = Post.objects.all().order_by('-id')[0:30]

        else:
            posts = Post.objects.all().order_by('-id')[0:30]

        context["posts"] = posts

        return context
    

class PostDetailView(DetailView):
    
    # new options for django201
    http_method_names = ['get']     # Default method = get
    template_name = 'feed/detail.html'

    model = Post
    context_object_name = "post" # this refers to context object default is "object"

 # new options for django201. in django101, we used FormView
class CreateNewPost(LoginRequiredMixin,CreateView):
    # LoginRequiredMixin = ensures user is logged in
    
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
    
    def post(self, request, *args: str, **kwargs: Any):
        
        # similar to django101 but mapping of data is from AJAX post request
        post = Post.objects.create(
            # from AJAX request
            text = request.POST.get("text"),
            author = request.user
        )

        # this is to override the standard POST request success_url='/' 
        return render(
            # HTTP request
            request,
            # string as html
            "includes/post.html",
            # context parameters of includes/post (post and show_detail_view)
            # {% include "includes/post.html" with post=post show_detail_view=True %}
            {
                "post": post,
                "show_detail_view": True
            },
            # content type
            content_type="application/html",
        )
    
    