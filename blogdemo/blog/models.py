from django.utils import timezone
from django.db import models

# Create your models here.
class Post(models):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
        
    
    class Meta:
        ordering: ['-publish']
        indexes = [
            models.Index((fields = ['-publish']),
        ]