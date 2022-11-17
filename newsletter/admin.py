from django.contrib import admin

from .models import Newsletter, NewsletterText

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('email',)
    ordering = ('-date_added',)
    date_hierarchy = 'date_added'
    readonly_fields = ('date_added',)
    fieldsets = (
        (None, {
            'fields': ('email', 'date_added')
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(NewsletterText)


