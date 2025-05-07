# blog/models.py

from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    tags = models.CharField(max_length=200, help_text="Enter comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
