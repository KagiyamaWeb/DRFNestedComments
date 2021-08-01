from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, MPTTComment
from .forms import PostForm

from django.utils import timezone
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView

from django.contrib.auth.models import User
from .serializers import PostSerializer, CommentFullSerializer, CommentGetSerializer, CommentPostSerializer

class PostListView(View):
    def get(self, request):
        posts = Post.objects.filter(date__lte=timezone.now()).order_by('-date')
        return render(request, 'blog/posts.html', {'posts': posts})

class PostDetail(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = MPTTComment.objects.filter(post = post)
        return render(request, 'blog/post_detail.html', {'post': post, 'comments' : comments})

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

class PostsAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        date = datetime.now()
        return serializer.save(author=author, date=date)
'''
class PostDetailAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, pk):
        post = Post.objects.filter(id=pk)
        serializer = PostSerializer(post)
        return Response({"comments": serializer.data})

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        #post = get_object_or_404(Post, id = self.request.data.get('post'))
        #parent = get_object_or_404(MPTTComment, id = self.request.data.get('parent'))
        #return serializer.save(author=author, post=post, parent=parent)
        return serializer.save(author=author)

class CommentsDetailAPIView(APIView):

    def get(self, request, pk):
        comments = MPTTComment.objects.filter(post=pk)
        serializer = CommentGetSerializer(comments, many=True)
        return Response({"comments": serializer.data})

    def perform_create(self, serializer):
        return serializer.save()
'''
class ThreeLevelCommentAPIView(ListCreateAPIView):

    queryset = MPTTComment.objects.all()
    serializer_class = CommentGetSerializer

    def get(self, request, pk):
        comments = MPTTComment.objects.filter(post=pk, level__lte=2)
        serializer = CommentGetSerializer(comments, many=True)
        return Response({"comments": serializer.data})

class PostCommentAPIView(ListCreateAPIView):

    queryset = MPTTComment.objects.all()
    serializer_class = CommentPostSerializer

    def perform_create(self, serializer):
        return serializer.save()    

class ThirdLevelDownAPI(ListCreateAPIView):

    queryset = MPTTComment.objects.all()
    serializer_class = CommentFullSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        return serializer.save(author=author)

