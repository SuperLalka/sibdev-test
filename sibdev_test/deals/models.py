from django.contrib.auth.models import User
from django.db import models

DEAL_TOTAL = "Total transaction amount"
DEAL_QUANTITY = "Total number of gems"


class Deal(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_deals')
    item = models.ForeignKey('Gem', on_delete=models.CASCADE, related_name='gem_deals')
    total = models.PositiveIntegerField(default=None, help_text=DEAL_TOTAL)
    quantity = models.PositiveSmallIntegerField(default=None, help_text=DEAL_QUANTITY)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} / {self.item} {self.total}"


class Gem(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
