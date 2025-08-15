from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)