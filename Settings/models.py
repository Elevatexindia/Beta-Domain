from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.admin.models import LogEntry as DjangoLogEntry
class SiteSetting(models.Model):
    show_preloader = models.BooleanField(default=True)

    def __str__(self):
        return f"Preloader is {'On' if self.show_preloader else 'Off'}"

    class Meta:
        app_label = 'Settings'
        verbose_name = "Preloader"
        verbose_name_plural = "Preloader Settings"




class LogEntry(DjangoLogEntry):
    class Meta:
        app_label = 'Settings'
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    expire_at = models.DateTimeField()
    is_terminated = models.BooleanField(default=False)

    # New fields added 👇
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_name = models.TextField(null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)

    def is_active(self):
        return not self.is_terminated and self.expire_at > timezone.now()

    def terminate(self):
        from django.contrib.sessions.models import Session
        try:
            session = Session.objects.get(session_key=self.session_key)
            session.delete()
        except Session.DoesNotExist:
            pass
        self.is_terminated = True
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.session_key}"

    class Meta:
        app_label = 'auth'    # Same as before
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
