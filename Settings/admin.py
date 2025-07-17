from django.contrib import admin
from django.shortcuts import redirect
from .models import SiteSetting
from django.urls import reverse
from .models import LogEntry
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry  #this will seprate the log entry from Settings app to the Adminstration
from django.contrib.contenttypes.models import ContentType
from .models import UserSession

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        try:
            setting = SiteSetting.objects.get()
            url = reverse('admin:Settings_sitesetting_change', args=[setting.id])  # <-- FIXED
            return redirect(url)
        except SiteSetting.DoesNotExist:
            return super().changelist_view(request, extra_context)



@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_link', 'action_flag', 'change_message')
    list_filter = ('action_flag', 'content_type', 'user')
    search_fields = ('object_repr', 'change_message','user')
    readonly_fields = [f.name for f in LogEntry._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == 3:  # deletion
            return obj.object_repr
        ct = obj.content_type
        try:
            url = reverse(f'admin:{ct.app_label}_{ct.model}_change', args=[obj.object_id])
            return format_html('<a href="{}">{}</a>', url, obj.object_repr)
        except:
            return obj.object_repr
    object_link.short_description = 'Object'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'ip_address', 'device_name', 'operating_system', 'start_time', 'last_activity', 'expire_at', 'is_active', 'terminate_session_button')
    readonly_fields = ('user', 'session_key', 'ip_address', 'device_name', 'operating_system', 'start_time', 'last_activity', 'expire_at', 'is_active', 'is_terminated')
    list_filter = ('is_terminated', 'start_time', 'expire_at', 'user','ip_address', 'device_name', 'operating_system')
    search_fields = ('user', 'ip_address', 'device_name', 'operating_system') 

    actions = ['terminate_selected_sessions']
    def has_add_permission(self, request):
        return False

    def terminate_selected_sessions(self, request, queryset):
        current_session_key = request.session.session_key
        for session in queryset.exclude(session_key=current_session_key):
            session.terminate()
        self.message_user(request, "Selected sessions (except current) terminated successfully.")
    terminate_selected_sessions.short_description = "Terminate selected sessions"

    def terminate_session_button(self, obj):
        if not obj.is_terminated:
            return format_html(
                '<a class="button" href="/admin/terminate_session/{}/">Terminate</a>', obj.id
            )
        return "-"
    terminate_session_button.short_description = 'Terminate Session'
    terminate_session_button.allow_tags = True



