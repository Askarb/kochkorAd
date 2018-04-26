from urllib.parse import urljoin

from django.conf import settings
from django.db import models

from main.media_path import ad_path
from webapp.utils import generate_slug


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='Link', unique=True)

    def __str__(self):
        return self.name


class AdManager(models.Manager):

    def get_queryset(self):
        return super(AdManager, self).get_queryset().all()

    def active(self, **kwargs):
        return super().get_queryset().filter(is_active=True, **kwargs)


class Ad(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(verbose_name='Text')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    rise_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    objects = AdManager()

    class Meta:
        ordering = ['-date_update']

    def save(self, force_insert=False, force_update=False, using=None, supdate_fields=None):

        while True:
            if not self.slug:
                self.slug = generate_slug(self.title)
            try:
                return super(Ad, self).save()
            except:
                self.slug = generate_slug(self.title)

    def increment_raise(self):
        self.rise_count += 1
        return self.rise_count

    def increment_view(self):
        self.view_count += 1
        return self.view_count

    def first_image(self):
        img = self.images.first()
        return img.image.url if img else urljoin(settings.STATIC_URL, 'img/no_image.png')


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE,)
    image = models.ImageField(upload_to=ad_path)

