from .models import Ad, Category, Application
from django.views.generic import TemplateView, FormView
from .forms import CreateAdForm
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_last_ads()
        context['categories'] = Category.objects.all()
        context['title'] = 'Акыркы жарнамалар!'
        return context

    def get_last_ads(self):
        paginator = Paginator(Ad.objects.all().filter(active=True).order_by('-date_update'), 5)
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
        context['item'] = Ad.objects.get(slug=self.get_ad_from_url())
        context['categories'] = Category.objects.all()
        return context

    def get_ad_from_url(self):
        if 'ad' in self.kwargs:
            return self.kwargs['ad']


class CategoryView(TemplateView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['items'] = self.get_ads_by_category()
        context['title'] = 'Категория боюнча жарнамалар!'
        return context

    def get_category_from_url(self):
        if 'category' in self.kwargs:
            return self.kwargs['category']

    def get_ads_by_category(self):
        paginator = Paginator(Ad.objects.all().filter(
            category=Category.objects.all().filter(slug=self.get_category_from_url())
        ).order_by('-date_update'), 5)
        page = self.request.GET.get('page')
        try:
            ads = paginator.page(page)
        except PageNotAnInteger:
            ads = paginator.page(1)
        except EmptyPage:
            ads = paginator.page(paginator.num_pages)
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
        self.alert_to_email(form)
        Application.objects.create(
            title=form.cleaned_data['title'],
            text=form.cleaned_data['text'],
            phone1=form.cleaned_data['phone1'],
            phone2=form.cleaned_data['phone2']
        )
        return super().form_valid(form)

    def alert_to_email(self, form):
        send_mail(
            'Kochkor ad: '+form.cleaned_data['title'],
            form.cleaned_data['text'],
            'kochkorjarnama@gmail.com',
            ['bolotbekov06@gmail.com'],
            fail_silently=False,
        )


class ThankView(TemplateView):
    template_name = 'thank.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context