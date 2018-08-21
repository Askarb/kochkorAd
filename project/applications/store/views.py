from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from applications.store.models import Goods
from applications.webapp.views import ContextMixin
from main.settings import ADS_PER_PAGE


class GoodsListView(ContextMixin, ListView):
    model = Goods
    template_name = 'store/objects_list.html'
    paginate_by = ADS_PER_PAGE
    queryset = model.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super(GoodsListView, self).get_context_data(**kwargs)
        context['title'] = _('Товары')
        return context


class GoodsView(ContextMixin, DetailView):
    model = Goods
    template_name = 'store/object.html'

    def get_context_data(self, **kwargs):
        context = super(GoodsView, self).get_context_data(**kwargs)
        context['suggests'] = Goods.suggest()
        return context
