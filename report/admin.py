# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import TableTitle, ColTitle, TableData, Nysc, Siwes


# Register your models here.
admin.site.register(TableTitle)
admin.site.register(ColTitle)
admin.site.register(TableData)
admin.site.register(Nysc)
admin.site.register(Siwes)