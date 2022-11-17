from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    intro = models.TextField()
    image = models.ImageField(upload_to='images/blog', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = RichTextUploadingField()
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')), default='draft')
    featured = models.BooleanField(default=False, null=True, blank=True)

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom managere
    tags = TaggableManager()


    class Meta:
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

# video/models.py
class Video(models.Model):
    title = models.CharField(max_length=100)
    intro = models.TextField()
    thumbnail = models.ImageField(upload_to='images/video', blank=True, default='images/video/default.jpg')
    publish = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')), default='draft')
    video_link = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_posts')



    class Meta:
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['publish']),
        ]

    def __str__(self):
        return self.title









