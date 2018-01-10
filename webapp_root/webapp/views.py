from time import time
from slugify import slugify, CYRILLIC
from .models import Ad, Category, AdImage
from django.views.generic import TemplateView, FormView
from .forms import CreateAdForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import telepot
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext as _
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_all_ads()
        context['categories'] = Category.objects.all()
        return context

    def get_all_ads(self):
        paginator = Paginator(Ad.objects.all().filter(active=True), 5)
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
        paginator = Paginator(Ad.objects.all().filter(active=True), 5)
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
            return Ad.objects.get(slug=self.kwargs['ad'])
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
            category=Category.objects.get(slug=self.kwargs['category']), active=True), 5)

        page = self.request.GET.get('page')
        try:
            ads = paginator.get_page(page)
        except PageNotAnInteger:
            ads = paginator.get_page(1)
        except EmptyPage:
            ads = paginator.get_page(paginator.num_pages)
        return ads


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
            slug=self.get_slug_link(form.cleaned_data['title']),
            text=form.cleaned_data['text'],
            category=form.cleaned_data['category'],
            date_create=timezone.now(),
            date_update=timezone.now(),
            phone1=form.cleaned_data['phone1'],
            phone2=form.cleaned_data['phone2'],
            active=False
        )
        for image in self.request.FILES.getlist('images'):
            AdImage.objects.create(ad=ad, image=image).save()

        self.send_notification_to_telegram(form)
        return super().form_valid(form)

    def send_notification_to_telegram(self, form):
        if not settings.DEBUG:
            token = '462585305:AAHk_kLP2kZhpAIA47iKldJuS4sOeJpcYIk'
            TelegramBot = telepot.Bot(token)
            TelegramBot.sendMessage(chat_id='@kochkor',
                                text='Title - {0}\r\nText - {1}'.format(form.cleaned_data['title'],
                                                                        form.cleaned_data['text']))

    def get_slug_link(self, title):
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
