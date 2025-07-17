from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import UserSession


# Create your views here.

def your_view(request):
    if request.session.get('session_terminated'):
        messages.error(request, "Your session was terminated by admin.")
        del request.session['session_terminated']
    # continue as normal


def terminate_session_admin(request, session_id):
    if not request.user.is_superuser:
        return redirect('admin:index')
    session = get_object_or_404(UserSession, id=session_id)
    session.terminate()
    messages.success(request, f"Session {session.session_key} terminated successfully.")
    return redirect('/admin/auth/usersession/')


