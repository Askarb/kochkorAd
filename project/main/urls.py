from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.urls import path, include

from applications.webapp.views import change_language

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n'), name='set_language'),
    path('change_language/', change_language, name='change_language'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^', include('applications.webapp.urls', namespace='webapp'))
)
