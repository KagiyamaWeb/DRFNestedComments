from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from mptt.models import MPTTModel, TreeForeignKey

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.date = timezone.now()
        self.save()

    def get_children(self):
        return MPTTComment.objects.filter(post=self)

    def get_third_level(self):
        tree_objs =  MPTTComment.objects.filter(post=self, level__lte=2)
        return (tree_objs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    comment_text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    
    def third_level_children(self):
        if self.level == 3:
            return self.get_children()

    def __str__(self):
        return f"Comment by {self.author}: {self.comment_text[0:40]}..." 

class MPTTComment(MPTTModel, Comment):
    """ Threaded comments - Add support for the parent comment store and MPTT traversal"""
    '''
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=True
    )
    # a link to comment that is being replied, if one exists
    '''
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    '''
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    '''
    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by=['date']

    class Meta:
        ordering=['tree_id','lft']

'''
class Reply(models.Model):
    comments = models.ForeignKey(Comment, related_name='replies',  on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = models.TextField()

    def __str__(self):
        return self.user.username

    @property
    def get_replies(self):
        return self.replies.all()

class Subscription(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
       return self.category
'''    