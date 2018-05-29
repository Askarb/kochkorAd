from . import views
from django.urls import path, re_path

app_name = 'webapp'

urlpatterns = (
    path('', views.HomeView.as_view(), name='index'),
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('ad/<slug:slug>/', views.AdView.as_view(), name='ad'),
    re_path('rise/ad/(?P<pk>\d+)/', views.RiseAdView.as_view(), name='rise_ad'),
    path('ad-create/', views.CreateAdView.as_view(), name='ad_create'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    # re_path('', BadURLView.as_view(), name='bad_url'),
)

