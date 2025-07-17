from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import ContactForm, NewsletterSubscription, PhoneCall, CustomerStats, UserProfile

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone_number', 'message')
    readonly_fields = ('name', 'email', 'phone_number', 'message', 'created_at')

    def has_add_permission(self, request):
        return False  # Disable the ability to add new ContactForm entries via admin

class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    search_fields = ['email']
    list_filter = ['subscribed_at']
    readonly_fields = ['subscribed_at']  # Ensure subscribed_at is read-only in admin

    def has_add_permission(self, request):
        return True  # Disables the ability to add new subscriptions via admin
        
class PhoneCallAdmin(admin.ModelAdmin):
    list_display = ('phone', 'scheduled_at')  # Display these fields in the list view
    search_fields = ('phone',)  # Add search capability by phone number
    list_filter = ('scheduled_at',)  # Add filter by scheduled date/time

    def has_add_permission(self, request):
        return True  # Disables the ability to add new subscriptions via admin
    
class CustomerStatsAdmin(admin.ModelAdmin):
    list_display = ('happy_clients', 'projects_completed', 'full_time_specialists', 'awards_won')    

admin.site.register(ContactForm, ContactFormAdmin)
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(PhoneCall)
admin.site.register(CustomerStats)

# Inline for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Extend User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


