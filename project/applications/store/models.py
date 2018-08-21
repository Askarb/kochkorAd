from urllib.parse import urljoin

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import strip_tags
from mptt.models import MPTTModel
from sorl.thumbnail import get_thumbnail

from applications.helpers.media_path import goods_image_path


class Category(MPTTModel):
    name = models.CharField(max_length=24)
    slug = models.SlugField()


class Store(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    info = RichTextField()
    phone = models.CharField(max_length=20)
    location = RichTextField()

    def __str__(self):
        return self.name


class Goods(models.Model):
    store = models.ForeignKey(Store, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=128)
    info = RichTextField()
    slug = models.SlugField()
    price = models.PositiveIntegerField()
    published = models.BooleanField(default=True, help_text='Опубликовать?')
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def first_image(self):
        img = self.images.first()
        return get_thumbnail(img.image, '250x195').url if img else urljoin(settings.STATIC_URL, 'img/no_image.png')

    def info_short(self):
        return strip_tags(self.info)[:80]

    @classmethod
    def suggest(cls, pk=0, count=3):
        return cls.objects.exclude(pk=pk).order_by('?')[:count]

    class Meta:
        ordering = ('priority', )


class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=goods_image_path)
