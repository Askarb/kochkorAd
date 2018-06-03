from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.views.i18n import set_language

from applications.webapp.forms import CreateAdForm, MessageCreateForm, AdImageFormset, AdPhoneFormset
from applications.webapp.models import Category, Ad, AdImage, Slider, Message, Variable
from applications.helpers.utils import send_notification_to_telegram
from main.settings import ADS_PER_PAGE


class ContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['meta'] =[
            ['title', Variable.objects.get(name='meta_title').value],
            ['description', Variable.objects.get(name='meta_description').value],
            ['keywords', Variable.objects.get(name='meta_keywords').value],
        ]
        return context


class HomeView(ContextMixin, ListView):
    template_name = 'home.html'
    model = Ad
    paginate_by = ADS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(active=True)
        context['title'] = _('Последние объявления')
        return context

    def get_queryset(self):
        return Ad.objects.active()


class AllAdView(ContextMixin, ListView):
    template_name = 'all_ad.html'
    model = Ad
    paginate_by = ADS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(AllAdView, self).get_context_data(**kwargs)
        context['title'] = _('Все объявления')
        return context

    def get_queryset(self):
        return Ad.objects.active()


class AdView(ContextMixin, DetailView):
    template_name = 'ad.html'
    model = Ad

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if not self.request.user.is_superuser:
            self.object.increment_view()
        return self.render_to_response(context)


class CategoryView(ContextMixin, ListView):
    template_name = 'category.html'
    model = Ad
    paginate_by = ADS_PER_PAGE

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['category'])
        category.increment_view(self.request)
        return Ad.objects.active().filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "%s: %s" % (_('Реклама по категориям'), Category.objects.get(slug=self.kwargs.get('category')))
        return context


class RiseAdView(View):
    success_message = _('Объявление успешно поднята!')

    def get(self, *args, **kwargs):
        try:
            return HttpResponseRedirect(reverse("webapp:ad", args=[Ad.objects.get(pk=kwargs['pk']).slug]))
        except Ad.DoesNotExist:
            return HttpResponseRedirect('/')

    def post(self, *args, **kwargs):
        try:
            ad = Ad.objects.get(pk=kwargs['pk'])
            ad.increment_raise()
            messages.add_message(self.request, messages.SUCCESS, self.success_message)
        except Ad.DoesNotExist:
            pass
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])


class CreateAdView(ContextMixin, CreateView):
    template_name = 'ad_create.html'
    form_class = CreateAdForm
    model = Ad
    success_message = _('Объявление успешно создана!')

    def get_context_data(self, **kwargs):
        context = super(CreateAdView, self).get_context_data(**kwargs)
        if self.request.POST:
            formset_img = AdImageFormset(self.request.POST, self.request.FILES)
            formset_phone = AdPhoneFormset(self.request.POST, self.request.FILES)
        else:
            formset_img = AdImageFormset()
            formset_phone = AdPhoneFormset()

        context['formset_img'] = formset_img
        context['formset_phone'] = formset_phone
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_img = context['formset_img']
        formset_phone = context['formset_phone']

        ad = form.save()
        if formset_img.is_valid():
            formset_img.instance = ad
            formset_img.save()

        if formset_phone.is_valid():
            formset_phone.instance = ad
            formset_phone.save()

        send_notification_to_telegram(self.request, form)
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return HttpResponseRedirect(reverse('webapp:ad', args=(ad.slug,)))

    def form_invalid(self, form):
        print(form)
        return super(CreateAdView, self).form_invalid(self.get_context_data())


class ContactView(ContextMixin, CreateView):
    template_name = 'contact.html'
    model = Message
    form_class = MessageCreateForm
    success_message = _('Сообщение успешно отправлено!')

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return self.request.META['HTTP_REFERER']


def change_language(request):
    if not request.POST:
        return redirect('/')
    return set_language(request)
