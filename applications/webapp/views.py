from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from applications.webapp.forms import CreateAdForm, MessageCreateForm
from applications.webapp.models import Category, Ad, AdImage, Slider, Message
from applications.helpers.utils import send_notification_to_telegram
from project.settings import ADS_PER_PAGE


class ContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title'] = _('Последние объявления')
        return context


class HomeView(ContextMixin, ListView):
    template_name = 'home.html'
    model = Ad
    paginate_by = ADS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(active=True)
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
        return Ad.objects.active().filter(category__slug=self.kwargs['category'])

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
            ad.date_update = timezone.now()
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

    def form_valid(self, form):
        form = form.save()
        for image in self.request.FILES.getlist('images'):
            AdImage.objects.create(ad=form, image=image).save()

        send_notification_to_telegram(self.request, form)

        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return HttpResponseRedirect(reverse('webapp:ad', args=(form.slug,)))


class ContactView(ContextMixin, CreateView):
    template_name = 'contact.html'
    model = Message
    form_class = MessageCreateForm
    success_message = _('Сообщение успешно отправлено!')

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return self.request.META['HTTP_REFERER']
