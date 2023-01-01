# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Company
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CompanyInLine(admin.StackedInline):
    model = Company
    can_delete=False
    verbose_name_plural = 'Companies'

class CustomizedUserAdmin (UserAdmin):
    inlines = (CompanyInLine,)

admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)

