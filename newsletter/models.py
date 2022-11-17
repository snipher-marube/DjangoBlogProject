from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Newsletter(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Newsletter'
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['email']),
        ]


class NewsletterText(models.Model):
    EMAIL_STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    subject = models.CharField(max_length=255, unique=True)
    body = RichTextUploadingField()
    email = models.ManyToManyField(Newsletter, blank=True)
    status = models.CharField(max_length=10, choices=EMAIL_STATUS_CHOICES, default='Draft')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = 'Newsletters'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['subject']),
        ]

