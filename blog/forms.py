from django import forms
from django.contrib.admin import widgets        
from .models import Post, MPTTComment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body',)