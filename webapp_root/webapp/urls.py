from . import views
from django.urls import path, re_path

app_name = 'webapp'

urlpatterns = (
    path('', views.IndexView.as_view(), name='index'),
    path('ad/', views.AllAdView.as_view(), name='all_ads'),
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('ad/<slug:slug>/', views.AdView.as_view(), name='ad'),
    re_path('rise/ad/(?P<pk>\d+)/', views.RiseAdView.as_view(), name='rise_ad'),
    path('adcreate/', views.CreateAdView.as_view(), name='ad_create'),
    path('success/', views.ThankView.as_view(), name='thank'),
    # re_path('', BadURLView.as_view(), name='bad_url'),
)

