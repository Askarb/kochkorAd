import telepot
from time import time
from .forms import CreateAdForm
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy
from slugify import slugify, CYRILLIC
from .models import Ad, Category, AdImage
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_all_ads()
        context['categories'] = Category.objects.all()
        return context

    def get_all_ads(self):
        paginator = Paginator(Ad.objects.all().filter(active=True), settings.ADS_PER_PAGE)
        page = self.request.GET.get('page')
        try:
            ads = paginator.page(page)
        except PageNotAnInteger:
            ads = paginator.page(1)
        except EmptyPage:
            ads = paginator.page(paginator.num_pages)
        return ads


class AllAdView(TemplateView):
    template_name = 'all_ads.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_all_ads()
        context['categories'] = Category.objects.all()
        context['title'] = _('Latest ads!')
        return context

    def get_all_ads(self):
        paginator = Paginator(Ad.objects.all().filter(active=True), settings.ADS_PER_PAGE)
        page = self.request.GET.get('page')
        try:
            ads = paginator.page(page)
        except PageNotAnInteger:
            ads = paginator.page(1)
        except EmptyPage:
            ads = paginator.page(paginator.num_pages)
        return ads


class AdView(TemplateView):
    template_name = 'Ad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.get_ad_from_url()
        context['categories'] = Category.objects.all()
        return context

    def get_ad_from_url(self):
        if Ad.objects.filter(slug=self.kwargs['ad']).count() > 0:
            ad = Ad.objects.get(slug=self.kwargs['ad'])
            if self.request.user.is_anonymous:
                ad.view_count += 1
                ad.save()
            return ad
        return None


class CategoryView(TemplateView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['items'] = self.get_ads_by_category()
        context['title'] = _('Ads by category!')
        return context

    def get_ads_by_category(self):
        paginator = Paginator(Ad.objects.filter(
            category=Category.objects.get(slug=self.kwargs['category']), active=True), settings.ADS_PER_PAGE)

        page = self.request.GET.get('page')
        try:
            ads = paginator.get_page(page)
        except PageNotAnInteger:
            ads = paginator.get_page(1)
        except EmptyPage:
            ads = paginator.get_page(paginator.num_pages)
        return ads


class RiseAdView(View):

    def get(self):
        return HttpResponseRedirect('/')

    def post(self, *args, **kwargs):
        try:
            ad = Ad.objects.get(pk=kwargs['pk'])
            ad.date_update = timezone.now()
            ad.rise_count += 1
            ad.save()
        except Ad.DoesNotExist:
            pass
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']


class CreationAdView(FormView):
    template_name = 'AdCreate.html'
    form_class = CreateAdForm
    success_url = reverse_lazy('webapp:thank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        ad = Ad.objects.create(
            title=form.cleaned_data['title'],
            slug=self.generate_slug(form.cleaned_data['title']),
            text=form.cleaned_data['text'],
            category=form.cleaned_data['category'],
            date_create=timezone.now(),
            date_update=timezone.now(),
            phone1=form.cleaned_data['phone1'],
            phone2=form.cleaned_data['phone2'],
            active=self.request.user.is_superuser
        )
        for image in self.request.FILES.getlist('images'):
            AdImage.objects.create(ad=ad, image=image).save()

        self.send_notification_to_telegram(form)
        return super().form_valid(form)

    def send_notification_to_telegram(self, form):
        if not self.request.user.is_authenticated:
            TelegramBot = telepot.Bot(settings.TELEGRAM_TOKEN)
            TelegramBot.sendMessage(chat_id='@kochkor',
                                text='Title - {0}\r\nText - {1}'.format(form.cleaned_data['title'],
                                                                        form.cleaned_data['text']))

    def generate_slug(self, title):
        return slugify((title + '-' + str(int(round(time()*1000)))), pretranslate=CYRILLIC)


class ThankView(TemplateView):
    template_name = 'thank.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BadURLView(TemplateView):
    template_name = 'page-404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
