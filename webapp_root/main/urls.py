from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include, re_path


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n'), name='set_language'),
    re_path('^', include('webapp.urls'), name='webapp'),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
