from rest_framework import serializers
from .models import MPTTComment, Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'date')

class CommentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPTTComment
        fields = ('id', 'comment_text', 'author', 'parent')
        depth = 3

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPTTComment
        fields = ('id', 'comment_text', 'author', 'parent', 'post')
    def create(self, validated_data):
        return MPTTComment.objects.create(**validated_data)

class CommentFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPTTComment
        fields = ['id', 'comment_text', 'author', 'parent']
        depth = 20
