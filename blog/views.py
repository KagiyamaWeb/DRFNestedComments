from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.views import View

class PostListView(View):
    def get(self, request):
        posts = Post.objects.filter(date__lte=timezone.now()).order_by('-date')
        return render(request, 'blog/posts.html', {'posts': posts})

class PostDetail(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

class PostNew(View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
'''
class Subscribe(View):
    def get(self, request, username):
        user = get_object_or_404(Profile, username=username)
        user.subscribers
'''
