# middleware.py

from django.utils import timezone
from .models import UserSession
from django.contrib.sessions.models import Session

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            if session_key:
                ip = self.get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')

                # Basic OS detection
                if 'Windows' in user_agent:
                    os = 'Windows'
                elif 'Macintosh' in user_agent:
                    os = 'macOS'
                elif 'Linux' in user_agent:
                    os = 'Linux'
                elif 'iPhone' in user_agent:
                    os = 'iOS'
                elif 'Android' in user_agent:
                    os = 'Android'
                else:
                    os = 'Unknown'

                user_session, created = UserSession.objects.get_or_create(
                    user=request.user,
                    session_key=session_key,
                    defaults={
                        'expire_at': timezone.now() + timezone.timedelta(hours=2),  # Set session expiry
                        'ip_address': ip,
                        'device_name': user_agent,
                        'operating_system': os
                    }
                )

                if user_session.is_terminated:
                    # Kill the session if admin has terminated it
                    from django.contrib.auth import logout
                    logout(request)
                    request.session.flush()
                    request.session['session_terminated'] = True
                else:
                    user_session.last_activity = timezone.now()

                    # Optional: update IP/device/OS every time, if you want real-time accuracy
                    user_session.ip_address = ip
                    user_session.device_name = user_agent
                    user_session.operating_system = os

                    user_session.save()
        return self.get_response(request)

    def get_client_ip(self, request):
        """Handle getting real IP behind proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

