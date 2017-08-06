from .models import Ad, Category, Application
from django.views.generic import TemplateView, FormView
from .forms import CreateAdForm
from django.core.urlresolvers import reverse_lazy

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Ad.objects.all().filter(active=True).order_by('-date_update')
        context['categories'] = Category.objects.all()
        context['title'] = 'Акыркы жарнамалар!'
        return context


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
        context['items'] = Ad.objects.all().filter(
            category=Category.objects.all().filter(slug=self.get_category_from_url())
        ).order_by('-date_update')
        context['title'] = 'Категория боюнча жарнамалар!'
        return context

    def get_category_from_url(self):
        if 'category' in self.kwargs:
            return self.kwargs['category']


class CreationAdView(FormView):
    template_name = 'AdCreate.html'
    form_class = CreateAdForm
    success_url = reverse_lazy('webapp:thank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        print(form.cleaned_data['title'], form.cleaned_data['text'])
        Application.objects.create(
            title=form.cleaned_data['title'],
            text=form.cleaned_data['text'],
            phone1=form.cleaned_data['phone1'],
            phone2=form.cleaned_data['phone2']
        )
        return super().form_valid(form)


class ThankView(TemplateView):
    template_name = 'thank.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context