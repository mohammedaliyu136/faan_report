# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class TableTitle(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class ColTitle(models.Model):
    title = models.CharField(max_length=100)
    field_type = models.CharField(max_length=30) 
    table_id = models.CharField(max_length=100)
    emp_field = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title+" "+str(self.table_id)


class TableData(models.Model): 
    col_id = models.CharField(max_length=100)
    row_id = models.CharField(max_length=100, default="1")
    table_id = models.CharField(max_length=100, default="1")
    data = models.CharField(max_length=100)

    month_d  =  models.CharField(max_length=25)
    quater_d =  models.CharField(max_length=25, default="nodate")
    year_d   =  models.CharField(max_length=25, default="nodate")


    def __str__(self):
        return str(self.id)+" "+str(self.pk)+" "+str(self.data)


class Nysc(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Siwes(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Todos(models.Model):
    data_id = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)
    effective_date = models.CharField(max_length=100)
    field_id = models.CharField(max_length=100)

    def __str__(self):
        return self.employee_id
