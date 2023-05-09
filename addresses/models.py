from django.db import models


class Addresses(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
