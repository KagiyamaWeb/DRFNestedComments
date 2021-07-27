from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
#from django.contrib.comments.models import Comment
#from mptt.models import MPTTModel, TreeForeignKey
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
        return MPTTComment.objects.filter(post=self)[:3]


    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    #parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    comment_text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
     
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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #subscriptions = models.ManyToManyField(Subscription)
    #subscribtions = models.ListField()
    subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    
    def subscribe(self, username):
        subscribers = get
'''    