# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Department, Designation, Profile, EducationInstitutions, AcademicProfessionalQualification
from django.http import JsonResponse
from employee.utils import *
import datetime




def get_emp(request, pk):
    e = Profile.objects.filter(employee_identification=pk)
    if(len(e) == 0):
        return JsonResponse({'status':'404'})
    else:
        name = e[0].firstname + " " +e[0].lastname
        dept = e[0].department
        dec = e[0].designation
        return JsonResponse({'status':'ok', 'name':name, "dept":dept, "dec":dec})

# Create your views here. 
def employee(request):
    return render(request, "employee/employee.html", {})

def employee_create(request):
    departments = Department.objects.all()
    return render(request, "employee/edit_employee.html", {"action":"createp", "departments":departments})

def employee_editt(request, pk, action):
    profile = ""
    education_institutions = ""
    academic_professional_qualification = ""
    if(action == "detail"):
        profile = Profile.objects.get(id=pk)
        education_institutions = EducationInstitutions.objects.filter(profile_id=pk)
        academic_professional_qualification = AcademicProfessionalQualification.objects.filter(profile_id=pk)
        action = "update"
        print education_institutions
        print academic_professional_qualification
    
    
    departments = Department.objects.all()
    if request.method == "POST":
        if(action == "createp"):
            profile_id = save_profile(request)
            ed_institution_ids = request.POST.get('ed_institution_ids')
            academic_form_ids = request.POST.get('academic_form_ids')
            save_educational_instition_attended(ed_institution_ids, request, profile_id)
            save_academic_professional_qualification(academic_form_ids, request, profile_id)
            

        elif(action == "update"):
            print "==================================="
            print pk
            profile = Profile.objects.get(id=pk)
            education_institutions = EducationInstitutions.objects.filter(profile_id=pk)
            academic_professional_qualification = AcademicProfessionalQualification.objects.filter(profile_id=pk)
        
            update_profile(request, profile.id)
            
            ed_institution_ids = request.POST.get('ed_institution_ids')
            academic_form_ids = request.POST.get('academic_form_ids')
            update_educational_instition_attended(ed_institution_ids, request, profile.id)
            update_academic_professional_qualification(academic_form_ids, request, profile.id)
            action="update"

        elif(action == "delete"):
            employee_del_id = request.POST.get('employee_del_id')
            profile = Profile.objects.get(id=employee_del_id).delete()
            education_institutions = EducationInstitutions.objects.filter(profile_id=employee_del_id).delete()
            academic_professional_qualification = AcademicProfessionalQualification.objects.filter(profile_id=employee_del_id).delete()



        #Profile(title=title, surname=surname, othername=other_name, maidenname=maiden_name, spouse_name=name_of_spouse, gender=gender,date_of_birth=date_of_birth, homeplace=place_of_birth, lga=lga, state=state_origin, country="country", status=marital_status, designation=designation, gl=grade_level, department="department", date_of_first_Appt=date_first_appt, date_of_conf=date_of_confirmation, name_employer=name_of_employer, date_of_transfer=date_of_transfer, pre_rank=rank, pre_gl=grade_level, pre_salary=salary_grade_level, date_of_last_promotion=last_promotion, staff_no=staff_no, account_num="account_num", occupant=True, nok_name_1=nok_name_1, nok_address_1=nok_address_1, nok_name_2=nok_name_2, nok_address_2=nok_address_2).save()
        return redirect("/employee/list")
    departments = Department.objects.all()
    return render(request, "employee/edit_employee.html", {"profile":profile, "departments":departments, "education_institutions":education_institutions, "academic_professional_qualifications":academic_professional_qualification, "action":action})

def employee_edit(request, pk):
    profile = Profile.objects.all()
    departments = Department.objects.all()
    if request.method == "POST":
        profile_id = save_profile(request)
        
        ed_institution_ids = request.POST.get('ed_institution_ids')
        academic_form_ids = request.POST.get('academic_form_ids')
        save_educational_instition_attended(ed_institution_ids, request, profile_id)
        save_academic_professional_qualification(academic_form_ids, request, profile_id)


        #Profile(title=title, surname=surname, othername=other_name, maidenname=maiden_name, spouse_name=name_of_spouse, gender=gender,date_of_birth=date_of_birth, homeplace=place_of_birth, lga=lga, state=state_origin, country="country", status=marital_status, designation=designation, gl=grade_level, department="department", date_of_first_Appt=date_first_appt, date_of_conf=date_of_confirmation, name_employer=name_of_employer, date_of_transfer=date_of_transfer, pre_rank=rank, pre_gl=grade_level, pre_salary=salary_grade_level, date_of_last_promotion=last_promotion, staff_no=staff_no, account_num="account_num", occupant=True, nok_name_1=nok_name_1, nok_address_1=nok_address_1, nok_name_2=nok_name_2, nok_address_2=nok_address_2).save()
        return redirect("/employee/list")
    return render(request, "employee/edit_employee.html", {"profile":profile, "departments":departments})


def employee_list(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        employeeFN = request.POST.get('employeeFN')
        employeeLN = request.POST.get('employeeLN')
        employeeHomeplace = request.POST.get('employeeHomeplace')
        employeeGender = request.POST.get('employeeGender')
        employeeStatus = request.POST.get('employeeStatus')
        employeeDoB = request.POST.get('employeeDoB')
        employeeDecoration = request.POST.get('employeeDecoration')
        employeeDepartment = request.POST.get('employeeDepartment')
        employeeID = request.POST.get('employeeID')

        dept_id = request.POST.get('employee_del_id')
        if (dept_id == 'new'):
            Profile(firstname=employeeFN, lastname=employeeLN, homeplace=employeeHomeplace, gender=employeeGender,
                    status=employeeStatus, date_of_birth=employeeDoB, decoration=employeeDecoration,
                    department=employeeDepartment, employee_identification=employeeID).save()
        else:
            dept_action = request.POST.get('dept_action')
            if dept_action == 'del':
                # del department
                Profile.objects.get(pk=int(dept_id)).delete()
            else:
                # edit department name
                print "edit department name"
                # d = Profile.objects.get(pk = int(dept_id))
                # d.name = dept_name
                # d.save()
    
    print "_____________________________"
    now = datetime.datetime.now()
    print str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    profile = Profile.objects.all()
    departments = Department.objects.all()
    designations = Designation.objects.all()
    context = {
        "profile": profile,
        "departments": departments,
        "designations": designations,
        "activate": "employee"
    }
    return render(request, "employee/employee_list.html", context)


def employee_detail(request, pk):
    profile = Profile.objects.get(id=pk)
    departments = Department.objects.all()
    return render(request, "employee/edit_employee.html", {"profile":profile, "departments":departments})

def employee_quater(request, pk):
    if request.method == 'POST':
        print "---------------------------------"
        print request.POST.get('quater')
    
    return JsonResponse({"status": "OK"})


def department(request):
    if request.method == 'POST':
        dept_name = request.POST.get('dept_name')
        dept_abbr = request.POST.get('dept_abbr')
        dept_id = request.POST.get('dept_name_old')
        if (dept_id == 'new'):
            Department(name=dept_name, abbr=dept_abbr, description='nill').save()
        else:
            dept_action = request.POST.get('dept_action')
            if dept_action == 'del':
                # del department
                Department.objects.get(pk=int(dept_id)).delete()
            else:
                # edit department name
                d = Department.objects.get(pk=int(dept_id))
                d.name = dept_name
                d.abbr = dept_abbr
                d.save()
    else:
        pass
    departments = Department.objects.all()
    context = {
        "departments": departments,
        "activate": "departments"
    }
    return render(request, "employee/department.html", context)


def designation(request):
    if request.method == 'POST':
        design_name = request.POST.get('design_name')
        design_dept = request.POST.get('design_dept')
        design_id = request.POST.get('design_id')
        if (design_id == "new"):
            Designation(name=design_name, department=design_dept).save()
        else:
            dept_action = request.POST.get('dept_action')
            if dept_action == 'del':
                # del department
                design_del_id = request.POST.get('design_del_id')
                Designation.objects.get(pk=int(design_del_id)).delete()
            else:
                # edit department name
                d = Designation.objects.get(pk=int(design_id))
                d.name = design_name
                d.department = design_dept
                d.save()

    departments = Department.objects.all()
    designation = Designation.objects.all()
    context = {
        "departments": departments,
        "designations": designation,
        "activate": "designations"

    }
    return render(request, "employee/designation.html", context)
