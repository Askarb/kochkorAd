from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from webapp.forms import CreateAdForm
from webapp.models import Category, Ad, AdImage
from webapp.utils import send_notification_to_telegram


class ContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class IndexView(ContextMixin, ListView):
    template_name = 'index.html'
    model = Ad
    paginate_by = 10


class AllAdView(ContextMixin, ListView):
    template_name = 'all_ads.html'
    model = Ad
    paginate_by = settings.ADS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Latest ads!')
        return context


class AdView(ContextMixin, DetailView):
    template_name = 'Ad.html'
    model = Ad


class CategoryView(ContextMixin, ListView):
    template_name = 'category.html'
    model = Ad
    paginate_by = 10

    def get_queryset(self):
        return Ad.objects.filter(category__slug=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Ads by category!')
        return context


class RiseAdView(View):

    def get(self, *args, **kwargs):
        try:
            return HttpResponseRedirect(reverse("webapp:ad", args=[Ad.objects.get(pk=kwargs['pk']).slug]))
        except Ad.DoesNotExist:
            return HttpResponseRedirect('/')

    def post(self, *args, **kwargs):
        try:
            ad = Ad.objects.get(pk=kwargs['pk'])
            ad.date_update = timezone.now()
            ad.rise_count += 1
            ad.save()
        except Ad.DoesNotExist:
            pass
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])


class CreateAdView(ContextMixin, CreateView):
    template_name = 'AdCreate.html'
    form_class = CreateAdForm
    model = Ad

    def form_valid(self, form):
        form = form.save()
        for image in self.request.FILES.getlist('images'):
            AdImage.objects.create(ad=form, image=image).save()

        send_notification_to_telegram(self.request, form)

        return HttpResponseRedirect(reverse('webapp:ad', args=(form.slug,)))


class ThankView(ContextMixin, TemplateView):
    template_name = 'thank.html'


class BadURLView(ContextMixin, TemplateView):
    template_name = 'page-404.html'
