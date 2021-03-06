import datetime
from urllib.parse import urljoin

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from sorl.thumbnail import get_thumbnail, ImageField

from applications.helpers.media_path import ad_path, slider_image_path
from applications.helpers.utils import generate_slug


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, verbose_name='Link', unique=True)
    view_count = models.IntegerField(default=0)

    def increment_view(self, request):
        if not request.user.is_staff:
            self.view_count += 1
            self.save()
        return self.view_count

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-view_count']


class AdManager(models.Manager):

    def get_queryset(self):
        return super(AdManager, self).get_queryset().all()

    def active(self, **kwargs):
        return super().get_queryset().filter(is_active=True, **kwargs).order_by('-date_update', '-date_create')


class Ad(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(verbose_name='Text')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rise_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    objects = AdManager()

    class Meta:
        ordering = ['-date_update']

    def number(self):
        return ', '.join(_.phone for _ in self.phones.all())

    def save(self, force_insert=False, force_update=False, using=None, supdate_fields=None):
        if not self.title:
            self.title = self.text[:20]

        if not self.date_update:
            self.date_update = datetime.datetime.now()

        while True:
            if not self.slug:
                self.slug = generate_slug(self.title)
            try:
                return super(Ad, self).save()
            except:
                self.slug = generate_slug(self.title)

    def increment_raise(self):
        self.rise_count += 1
        self.date_update = datetime.datetime.now()
        self.save()
        return self.rise_count

    def increment_view(self):
        self.view_count += 1
        self.save()
        return self.view_count

    def first_image(self):
        img = self.images.first()
        return get_thumbnail(img.image, '250x195').url if img else urljoin(settings.STATIC_URL, 'img/no_image.png')

    @classmethod
    def suggest(cls, pk=0, count=3):
        date = datetime.datetime.now()-datetime.timedelta(days=10)
        return Ad.objects.exclude(pk=pk).filter(date_update__gte=date).order_by('?')[:count]

    def __str__(self):
        return str(self.title)

    # @classmethod
    # def random_items(cls):
    #     item_count = 3
    #     cls.objects.first()


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE,)
    image = ImageField(upload_to=ad_path)


class AdPhone(models.Model):
    ad = models.ForeignKey(Ad, related_name='phones', on_delete=models.CASCADE,)
    phone = models.CharField(max_length=20)

    # class Meta:
    #     unique_together = ('ad', 'phone')


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


class Track(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
