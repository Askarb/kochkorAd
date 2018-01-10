from django.urls import path, re_path
from .views import IndexView, AllAdView, CategoryView, AdView, CreationAdView, ThankView, BadURLView
from django.utils.translation import gettext_lazy as _


app_name = 'webapp'
urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('ad/', AllAdView.as_view(), name='all_ads'),
    path('category/<slug:category>/', CategoryView.as_view(), name='category'),
    path('ad/<slug:ad>/', AdView.as_view(), name='ad'),
    path('adcreate/', CreationAdView.as_view(), name='ad_create'),
    path('success/', ThankView.as_view(), name='thank'),
    # re_path('', BadURLView.as_view(), name='bad_url'),
)

