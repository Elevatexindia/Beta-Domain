from django.contrib import admin
from .models import BlogModel

@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'keywords', 'views')  # Show views
    search_fields = ('title', 'slug', 'user__username', 'keywords', 'description')
    list_filter = ('created_at', 'updated_at', 'user')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'views')  # Make views read-only
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'image', 'keywords', 'description', 'views')
        }),
        ('Author & Timing Info', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
    )
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
