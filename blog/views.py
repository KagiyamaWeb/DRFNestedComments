from django.shortcuts import render
from .models import Post
from django.utils import timezone

def post_list(request):
    posts = Post.objects.filter(date__lte=timezone.now()).order_by('date')
    return render(request, 'blog/posts.html', {'posts': posts})
