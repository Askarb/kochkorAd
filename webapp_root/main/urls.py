from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include, re_path


urlpatterns =[
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n'), name='set_language')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    re_path('^', include('webapp.urls', namespace='webapp'))
)
