from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, View, CreateView
from django.contrib.auth.models import User
from feed.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from followers.models import Follower


# Create your views here.
class ProfileDetailView(DetailView):
    
    http_method_names = ['get']     # Default method = get
    template_name = 'profiles/detail.html'

    model = User # from django.contrib.auth.models
    context_object_name = "user"

    slug_field = "username"
    # from urls.py urlpatterns
    slug_url_kwarg = "username"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):

        # user = username (slug field / slug url)
        user = self.get_object()

        context = super().get_context_data(**kwargs)
        context["total_posts"] = Post.objects.filter(author = user ).count()
        # TODO Add total followers

        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by=self.request.user).exists()
        return context
    
class FollowView(LoginRequiredMixin,View):
    http_method_names = ['post']     # Only post request

    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        
        # data field from AJAX request
        data = request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
        
        try:
            user_to_be_followed = User.objects.get(username=data.get('username'))
        
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing data")

        if data.get('action') == "follow":
            #Follow
            follower, created = Follower.objects.get_or_create(
                followed_by = request.user,
                following = user_to_be_followed
            )

        else:
            #Unfollow
            try:
                follower = Follower.objects.get(
                    followed_by = request.user,
                    following = user_to_be_followed
                )
            except Follower.DoesNotExist:
                return HttpResponseBadRequest("Missing data")

            if follower:
                follower.delete()

        # Return json response this will be pushed back to AJAX success/error codes
        return  JsonResponse(
            {
                'success': True,
                'wording': "Unfollow" if data['action'] == "follow" else "Follow"
            }   
        )