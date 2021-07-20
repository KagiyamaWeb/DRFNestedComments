from django.db import models
from django.utils import timezone

# Create your models here.
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


    def __str__(self):
        return self.title