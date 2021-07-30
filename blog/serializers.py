from rest_framework import serializers
from .models import MPTTComment, Post
'''
class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    #date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z")
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'date')
'''
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'date')

class CommentSerializer(serializers.ModelSerializer):
    def get_replies(self, obj):
        queryset = MPTTComment.objects.filter(parent_id=obj.id)
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = MPTTComment
        fields = ('id', 'comment_text', 'author', 'parent', 'post')
