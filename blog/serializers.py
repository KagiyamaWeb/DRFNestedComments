from rest_framework import serializers
from .models import MPTTComment, Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'date')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPTTComment
        fields = ['id', 'comment_text', 'author', 'parent', 'post']
        depth = 3

class CommentFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPTTComment
        fields = ['id', 'comment_text', 'author', 'parent', 'post']
        #depth = 3
