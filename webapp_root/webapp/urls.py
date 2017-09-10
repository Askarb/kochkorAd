
from django.conf.urls import url
from .views import IndexView, CategoryView, AdView, CreationAdView, ThankView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category>[\w-]+)/$', CategoryView.as_view(), name='category'),
    url(r'^ad/(?P<ad>[\w-]+)/$', AdView.as_view(), name='ad'),
    url(r'^adcreate/$', CreationAdView.as_view(), name='adCreate'),
    url(r'^success/$', ThankView.as_view(), name='thank'),
]

