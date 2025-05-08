from django.db import models
from taggit.managers import TaggableManager

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    tags = TaggableManager()  # <-- add this line

    def __str__(self):
        return self.title
