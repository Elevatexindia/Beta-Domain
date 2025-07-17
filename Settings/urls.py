# Settings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('admin/terminate_session/<int:session_id>/', views.terminate_session_admin, name='terminate_session_admin'),
]
