from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=20)
    val = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Account(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def sum(self):
        tr = self.transaction_set.last()
        if tr:
            return tr.sum
        return 0


class Transaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    sum = models.FloatField(default=0)
    amount = models.FloatField()
    info = models.TextField(blank=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}|{}".format(self.account.name, self.amount)

    @property
    def account__sum(self):
        return self.account.sum

    def in_som(self):
        return self.amount * self.account.currency.val

    def save(self, **kwargs):
        if self.sum == 0:
            self.sum = self.account.sum + self.amount
        return super(Transaction, self).save()
