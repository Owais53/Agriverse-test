# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username
