from django.contrib import admin
from .models import Comment, Post, MPTTComment
from .models import Post

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(MPTTComment)



