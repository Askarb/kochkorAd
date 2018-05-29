from urllib.parse import urljoin

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from sorl.thumbnail import get_thumbnail

from applications.helpers.media_path import ad_path, slider_image_path
from applications.helpers.utils import generate_slug


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
        if not self.title:
            self.title = self.text[:20]

        while True:
            if not self.slug:
                self.slug = generate_slug(self.title)
            try:
                return super(Ad, self).save()
            except:
                self.slug = generate_slug(self.title)

    def increment_raise(self):
        self.rise_count += 1
        self.save()

    def increment_view(self):
        self.view_count += 1
        self.save()

    def first_image(self):
        img = self.images.first()
        return get_thumbnail(img.image, '250x195', crop='center', quality=99).url if img else urljoin(settings.STATIC_URL, 'img/no_image.png')

    def __str__(self):
        return str(self.title)


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE,)
    image = models.ImageField(upload_to=ad_path)


class Slider(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    text = RichTextField()
    image = models.ImageField(upload_to=slider_image_path)
    active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return self.title


class Variable(models.Model):
    name = models.CharField(max_length=64, unique=True)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Message(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=16)
    message = models.TextField()

    def __str__(self):
        return self.name
