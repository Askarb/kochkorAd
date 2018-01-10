from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='Link', unique=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, unique=True, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    text = models.TextField(verbose_name='Text')
    date_create = models.DateTimeField()
    date_update = models.DateTimeField()
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_update']


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='ad')

