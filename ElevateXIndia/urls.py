from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from Settings import views

urlpatterns = [
    path('admin/terminate_session/<int:session_id>/', views.terminate_session_admin, name='terminate_session_admin'),
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),  # Django JET
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # JET Dashboard
    path('', include('Main.urls')),
    path('', include('Settings.urls')),
    path('', include('Blog.urls')),
    path('froala_editor/', include('froala_editor.urls')),
    path('api/', include('Blog.urls_api')),
]

# Custom 404 handler
handler404 = 'Main.views.Page404'

# Serve media and static in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
