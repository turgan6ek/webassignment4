from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .forms import PostForm
from .serializers import PostSerializer, PostV2Serializer


# Custom decorator for admin access
def admin_required(view_func):
    decorator = user_passes_test(lambda u: u.is_superuser)
    return decorator(view_func)


@admin_required
def admin_view(request):
    # Admin-specific logic
    pass


# List all posts
@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'blog/post_list.html', {'posts': posts})


# View details of a single post
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# Create a new post
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# Admin-specific view
@admin_required
def admin_view(request):
    return render(request, 'blog/admin_dashboard.html')  # Replace with your admin dashboard template


# Custom login view with role-based redirection
class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/admin/'  # Redirect admin to admin dashboard
        return '/post/'  # Redirect regular users to post list


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostV2ViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostV2Serializer

class BurstRateThrottle(UserRateThrottle):
    rate = '5/min'  # Limit to 5 requests per minute for bursts

class PostViewSet(viewsets.ModelViewSet):
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        throttle_classes = [BurstRateThrottle]  # Apply the custom throttle
