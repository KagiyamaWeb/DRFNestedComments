from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, MPTTComment
from .forms import PostForm

from django.utils import timezone
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView

from django.contrib.auth.models import User
from .serializers import PostSerializer, CommentSerializer

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
        return serializer.save(author=author)

class PostDetailAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        return serializer.save(author=author)

class CommentsDetailAPIView(APIView):

    def get(self, request, pk):
        comments = MPTTComment.objects.filter(post=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        #post = get_object_or_404(Post, id = self.request.data.get('post'))
        #parent = get_object_or_404(MPTTComment, id = self.request.data.get('parent'))
        #return serializer.save(author=author, post=post, parent=parent)
        return serializer.save(author=author)

class ThreeLevelCommentAPIView(APIView):

    def get(self, request, pk):
        comments = MPTTComment.objects.filter(post=pk, level__lte=2)
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        return serializer.save(author=author)

class ThirdLevelDownAPI(APIView):

    def get(self, request, pk, cpk):
        comments = get_object_or_404(MPTTComment, post=pk, id=cpk).get_children()
        #comments = MPTTComment.objects.filter(post=pk, parent=cpk)
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        return serializer.save(author=author)

