from django.contrib import admin
from django.utils.html import format_html

from .models import Post, Comment, Contact, Video

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # car thumbnail
    def thumbnail(self, object):
        return format_html(f'<img src="{object.image.url}" width="40px" >')
    list_display = ('thumbnail', 'title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    search_fields = ('name', 'email', 'subject', 'message')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', 'publish', 'status')
    list_filter = ('status', 'publish')
    search_fields = ('title', 'intro')
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


