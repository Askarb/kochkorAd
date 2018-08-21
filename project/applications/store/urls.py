from django.urls import path

from applications.store.views import GoodsListView, GoodsView

app_name = 'store'


urlpatterns = [
    path('', GoodsListView.as_view(), name='goods_list'),
    path('/goods/<slug:slug>/', GoodsView.as_view(), name='goods'),
]
