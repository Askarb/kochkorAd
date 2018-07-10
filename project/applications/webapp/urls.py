from . import views
from django.urls import path, re_path

app_name = 'webapp'

urlpatterns = (
    path('', views.HomeView.as_view(), name='index'),
    path('all', views.AllAdView.as_view(), name='all_ad'),
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('ad/<slug:slug>/', views.AdView.as_view(), name='ad'),
    re_path('rise/ad/(?P<pk>\d+)/', views.RiseAdView.as_view(), name='rise_ad'),
    path('ad-create/', views.CreateAdView.as_view(), name='ad_create'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('whatsapp/', views.TrackView.as_view(), name='whatsapp'),
    path('whatsapp-create/', views.track_create, name='track_create'),
)

