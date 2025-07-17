from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *
from django.contrib.auth.models import User
from django.utils.text import slugify  # Optional if you use custom slug logic

class BlogModel(models.Model):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True, blank=True, unique=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)  # New field
    description = models.TextField(blank=True, null=True)  # New field
    views = models.PositiveIntegerField(default=0)  # New field for view count

    class Meta:
        verbose_name = 'Blog Entries'
        verbose_name_plural = 'Blog Entries'
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title)  # You must define this function
        super(BlogModel, self).save(*args, **kwargs)
    