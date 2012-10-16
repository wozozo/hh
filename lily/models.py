# coding: utf-8

from django import models
from django.utils import timezone


class DateTimeModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    deleted = models.DateTimeField(default='null', null=True)
