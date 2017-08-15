from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='Link', unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category)
    text = RichTextField(verbose_name='Text')
    date_create = models.DateTimeField()
    date_update = models.DateTimeField()
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True)
    active = models.BooleanField(default=True)


class Application(models.Model):
    title = models.CharField(max_length=150, blank=True)
    text = RichTextField(verbose_name='Text', blank=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    checked = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

