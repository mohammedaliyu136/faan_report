# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length = 300)
    description = models.CharField(max_length = 1000, null=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    name = models.CharField(max_length = 300)
    department = models.CharField(max_length = 300, null=True)

    def __str__(self):
        return self.name+" - "+self.department

class EducationInstitutions(models.Model):
    profile_id = models.CharField(max_length = 10)
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 300)
    from_date = models.CharField(max_length = 30)
    to_date = models.CharField(max_length = 30)

    def __str__(self):
        return self.name+" - "+str(self.from_date)+" - "+str(self.to_date)

class AcademicProfessionalQualification(models.Model):
    profile_id = models.CharField(max_length = 10)
    name = models.CharField(max_length = 30)
    date = models.CharField(max_length = 30)

    def __str__(self):
        return self.name+" - "+str(self.date)       

class Profile(models.Model):
    title = models.CharField(max_length = 10)
    surname = models.CharField(max_length = 100) 
    othername = models.CharField(max_length = 100)
    maidenname = models.CharField(max_length = 100, blank=True)

    spouse_name = models.CharField(max_length=30, blank=True)

    gender = models.CharField(max_length = 20)

    date_of_birth = models.CharField(max_length = 20)

    homeplace = models.TextField()

    lga = models.CharField(max_length = 30)
    state = models.CharField(max_length = 30)
    country = models.CharField(max_length = 30)
    phone_1 = models.CharField(max_length = 30, blank=True)
    phone_2 = models.CharField(max_length = 30, blank=True)

    status = models.CharField(max_length = 20)
    designation = models.CharField(max_length = 20)
    gl = models.CharField(max_length = 20)
    department = models.CharField(max_length = 40)

    date_of_first_Appt = models.CharField(max_length = 20)
    date_of_conf = models.CharField(max_length = 20)

    #if your service is transfered to FAAN
    name_employer = models.CharField(max_length =  20, blank=True)
    date_of_transfer = models.CharField(max_length = 20, blank=True)
    pre_rank = models.CharField(max_length=20, blank=True)
    pre_gl = models.CharField(max_length = 20)

    pre_salary =  models.CharField(max_length=20, blank=True)
    date_of_last_promotion = models.CharField(max_length = 20, blank=True)
    staff_no = models.CharField(max_length=30, blank=True)

    account_num = models.CharField(max_length = 30, blank=True)

    occupant = models.BooleanField()


    # Next of kin 1
    nok_name_1 = models.CharField(max_length=30, blank=True)
    nok_address_1 = models.CharField(max_length=45, blank=True)
    nok_relationship_1 = models.CharField(max_length=45, blank=True)
    # Next of kin 2
    nok_name_2 = models.CharField(max_length=30, blank=True)
    nok_address_2 = models.CharField(max_length=45, blank=True)
    nok_relationship_2 = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.othername+" - "+self.surname+" - "+self.department
