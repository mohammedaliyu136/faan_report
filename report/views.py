# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from report.utils import *
from .models import TableTitle, ColTitle, TableData, Nysc, Siwes
from employee.models import Department, Profile, AcademicProfessionalQualification
from report.reports_temp import StaffMovementSummaryReport, MonthlyTrainingMatterReport

import datetime


# Create your views here.
def index(request, pk, time):
    print "-----------------------------------"
    print "-----------------------------------"
    print time, pk
    mydatee = datetime.datetime.now()
    mon = mydatee.strftime("%B")
    yr = mydatee.strftime("%Y")
    if pk=="current":
        pk=mon+"_"+yr
    print "-----------------------------------"
    print "-----------------------------------"

    tables = TableTitle.objects.all()
    data_p = TableData.objects.values('month_d', 'year_d').distinct()
    r = pk.split("_")
    if len(r)>1:
        pk = r[0]
        year = r[1]
    else:
        year = ""
    return render(request, "report/index.html", {"tables":tables, "time":time, "name":pk, "data_p":data_p, "year":year})

def select_month_report(request):
    month = "current"
    if request.POST:
        month = request.POST.get("month_select")
    return redirect("/report/month/"+month+"/")

def monthly_list(request):
    data_p = TableData.objects.values('month_d', 'year_d').distinct()
    return render(request, 'report/monthly.html', {"data":data_p})

def quater(request):
    data_p = TableData.objects.values('quater_d', 'year_d').distinct()
    print data_p
    return render(request, 'report/quaterly.html', {"data":data_p})

def annual(request):
    data_p = TableData.objects.values('year_d').distinct()
    print data_p
    return render(request, 'report/annually.html', {"data":data_p})


def detail(request, pk, time, name):

    t = TableTitle.objects.get(id=pk)
    title = TableTitle.objects.get(title=t.title)
    col = ColTitle.objects.filter(table_id = str(title.pk))
    departments = Department.objects.all()
    if request.method == 'POST':
        if request.POST.get("del_report"):
            report_edit_id = request.POST.get("report_del_id")
            report_edit_id = report_edit_id.split(",")
            report_edit_id.pop()
            for rep in report_edit_id:
                TableData.objects.get(id=int(rep)).delete()
        elif request.POST.get("action"):
            report_edit_id = request.POST.get("report_edit_id")
            report_edit_id=report_edit_id.split(",")
            for i in xrange(0,len(report_edit_id)):
                tableData = TableData.objects.get(id=int(report_edit_id[i]))
                tableData.data = request.POST.get(str(i+1))


                tableData.save()
        else:
            rep_data = []
            for c in col:
                if(c.emp_field):
                    d = request.POST.get(c.emp_field)
                else:
                    d = request.POST.get(c.title)

                    mydatee = datetime.datetime.now()

                    mon = mydatee.strftime("%B")

                    mydate = mydatee.month
                    myear = mydatee.year
                    if mydate in range(1,3):
                        quater_str = "Q1"
                    elif mydate in range(4,6):
                        quater_str = "Q2"
                    elif mydate in range(7,9):
                        quater_str = "Q3"
                    elif mydate in range(10,12):
                        quater_str = "Q4"

                TableData(col_id=c.id, data=d, table_id=t.id, month_d = mon, quater_d = quater_str, year_d = myear).save()
                rep_data.append([c.title, d])

            update_employee(title, rep_data, request.POST.get('emp_id'))

    if(time=="month"):
        if(name=="current"):
            mydatee = datetime.datetime.now()
            mon = mydatee.strftime("%B")
            yr = mydatee.strftime("%Y")
            data = TableData.objects.filter(table_id = str(title.pk), month_d=mon, year_d=yr)
        else:
            data = TableData.objects.filter(table_id = str(title.pk), month_d=name.split("_")[0], year_d=name.split("_")[1])
    elif(time=="quater"):
        name_data = name.split("_")
        qtr = name_data[0]
        yr = name_data[1]
        data=TableData.objects.filter(table_id=str(title.pk), quater_d=qtr, year_d=yr)
    elif(time=="annual"):
        data = TableData.objects.filter(table_id = str(title.pk), year_d=name)

    row = []
    for i in xrange(0,len(data),len(col)):
        row.append([])
        d=[]
        id_s = []
        for j in xrange(0, len(col)):
            d.append(data[i+j].data)
            id_s.append(data[i+j].id)
        row[-1].append(d)
        row[-1].append(id_s)
    print row
    print data
    print TableData.objects.all()
    print name
    return render(request, "report/detail.html", {"tiltle":t, "cols":col, "data":data, "rows":row, "departments":departments, "pk":pk, "time":time, "name":name})

def hardcopy(request, time, value, pk):
    t = TableTitle.objects.get(id=pk)
    title = TableTitle.objects.get(title=t.title)
    col = ColTitle.objects.filter(table_id = str(title.pk))
    departments = Department.objects.all()
    if request.method == 'POST':
        for c in col:
            d = request.POST.get(c.title)
            TableData(col_id=c.id, data=d, table_id=t.id).save()

    if(time=="month"):
        if(value=="current"):
            mydatee = datetime.datetime.now()
            mon = mydatee.strftime("%B")
            data=TableData.objects.filter(table_id=str(title.pk), month_d=mon)
        else:
            data=TableData.objects.filter(table_id=str(title.pk), month_d=value)
    elif(time=="quater"):
        name_data = value.split("_")
        qtr = name_data[0]
        yr = name_data[1]
        data=TableData.objects.filter(table_id=str(title.pk), quater_d=qtr, year_d=yr)
    elif(time=="annual"):
        data=TableData.objects.filter(table_id=str(title.pk), year_d=value)
    #data = TableData.objects.filter(table_id = str(title.pk), )
    row = []
    for i in xrange(0,len(data),len(col)):
        row.append([])
        d=[]
        id_s = []
        for j in xrange(0, len(col)):
            d.append(data[i+j].data)
            id_s.append(data[i+j].id)
        row[-1].append(d)
        row[-1].append(id_s)
    return render(request, "report/hardcopy/index.html", {"tiltle":t, "cols":col, "data":data, "rows":row, "departments":departments})

def default_hardcopy(request, pk, name, time):
    departments = Department.objects.all()
    profile_count = Profile.objects.all().count()

    # ..manpower report..
    table = ""
    manPowerReport = []
    staff_movement_summary_data = []
    monthly_training_matter_data = []
    lastline = [
        [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]
    ]
    if(int(pk)==1):
        table = "existing_manpower_disposition"
        staff_list_report_gen(departments, manPowerReport, lastline)

    # ..staff_movement_summary report..
    if(int(pk)==2):
        table = "staff_movement_summary_analysis"
        staff_movement_summary(departments, staff_movement_summary_data)
    # ..monthly_training_matter report..
    if(int(pk)==3):
        table = "monthly_report_trainning_matters"
        monthly_training_matter(departments, monthly_training_matter_data)

    context = {

        "manPowerReport": manPowerReport,
        "lastline": lastline,

        "staff_movement_summary_data": staff_movement_summary_data,
        "monthly_training_matter_data": monthly_training_matter_data,

        "table": table,

        #"retirement":retirement,
        "profile_count":profile_count,

        "activate": "monthly"
    }

    return render(request, 'report/hardcopy/default/index.html', context)

def staff_list_new(request):
    departments = Department.objects.all()
    context = {
        "departments": departments,
        "activate": "staff_list_rep",
        "report_name": "Staff List Grouped by Department",
        "url_snip": "staff/list"
    }
    return render(request, "report/staff_list.html", context)

def staff_list_detail_new(request, pk):
    department = Department.objects.get(id=pk)
    departments = Department.objects.all()
    profiles = Profile.objects.filter(department=department)
    dddd = []
    gls = [18,17,16,15,14,13,12,11,10,"09","08","07","06","05","04","03","02","01"]
    for gl in gls:
        for p in profiles:
            if p.gl.split("/")[0]==str(gl):
                dddd.append(p)
    profiles=dddd
    #print profile_t
    #profiles=profile_t
    profiles_data =[]
    for profile in profiles:
        profile_tem = Profile_template(name=profile.surname+" "+profile.othername+" "+profile.maidenname,
                         title=profile.title,
                         sex=profile.gender,
                         date_of_birth=profile.date_of_birth,
                         staff_no=profile.staff_no,
                         designation=profile.designation,
                         gl=profile.gl,
                         date_of_first_Appt=profile.date_of_first_Appt,
                         date_of_conf=profile.date_of_conf,
                         date_of_last_promotion=profile.date_of_last_promotion,
                         lga=profile.lga,
                         state_of_origin=profile.state,
                         department=profile.department,
                         id=profile.id)
        academicProfessionalQualification = AcademicProfessionalQualification.objects.filter(profile_id=profile.id)
        profile_tem.set_qualification_with_date(academicProfessionalQualification)
        profiles_data.append(profile_tem)

    context = {
        #"profiles": profiles,
        "profiles": profiles_data,
        "dept": department,
        "departments": departments,
        "activate": pk,
        "report_name": "Staff List Grouped by Department",
        "url_snip": "staff/list"
    }
    return render(request, "report/hardcopy/staff_list/staff_list2.html", context)

def audit_staff_list_detail_new(request, pk):
    department = Department.objects.get(id=pk)
    departments = Department.objects.all()
    #profiles = Profile.objects.order_by('pre_gl').filter(department=department)
    profiles = Profile.objects.filter(department=department)
    dddd = []
    gls = [18,17,16,15,14,13,12,11,10,"09","08","07","06","05","04","03","02","01"]
    for gl in gls:
        for p in profiles:
            if p.gl.split("/")[0]==str(gl):
                dddd.append(p)
    profiles=dddd

    context = {
        "profiles": profiles,
        "dept": department,
        "departments": departments,
        "activate": pk,
        "report_name": "Audit of Staff List Grouped by Department",
        "url_snip": "audit/list"
    }
    return render(request, "report/hardcopy/audit/audit2.html", context)


def audit_staff_list_new(request):
    departments = Department.objects.all()
    context = {
        "departments": departments,
        "activate": "audit_staff_list_rep",
        "report_name": "Audit of Staff List Grouped by Department",
        "url_snip": "audit/list"
    }
    return render(request, "report/staff_list.html", context)


def staff_list_report(request):
    #discipline = Disciplinary.objects.all()
    departments = Department.objects.all()
    #name_change = Name_change.objects.all()
    #marraige_status = Marraige_status.objects.all()
    profile = Profile.objects.all().order_by("pre_gl")

    # ..manpower report..
    manPowerReport = []
    lastline = [
        [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]
    ]
    manpower(departments, manPowerReport, lastline)
    print lastline
    print "==============******================="
    pp = []
    for p in profile:
        emp_id = p.id
        academicProfessionalQualification = AcademicProfessionalQualification.objects.filter(profile_id=emp_id)
        profile_template = Profile_template(p.surname+" "+p.othername+" "+p.maidenname, p.title, p.gender, p.date_of_birth, p.staff_no, p.designation, p.pre_gl, p.date_of_first_Appt, p.date_of_conf, p.date_of_last_promotion, p.lga, p.state, p.department)
        profile_template.set_qualification_with_date(academicProfessionalQualification)
        pp.append(profile_template)
        print academicProfessionalQualification
        print profile_template.qualification_with_date


    context = {
        "pp": profile,
        #"discipline": discipline,
        "departments": departments,
        #"name_change": name_change,
        #"marraige_status": marraige_status,
        "profile":pp,

        "manPowerReport": manPowerReport,
        "lastline": lastline,

        "activate": "staff_list"
    }
    return render(request, "report/hardcopy/staff_list/index.html", context)

def audit(request):
    profile = Profile.objects.all()
    departments = Department.objects.all()
    context = {
        "profile": profile,
        "departments": departments,
        "activate": "audit"
    }
    return render(request, 'report/hardcopy/audit/index.html', context)


def report_json_final(request, time, name):
    res = ""
    if(time=="month"):
        departments = Department.objects.all()
        manPowerReport = []
        # ..manpower report..
        manpower = manpower_disposition(departments, manPowerReport)
        res = generate_monthly_report(request, name, manpower)
    elif(time=="quater"):
        q = name.split("_")[0]
        y = name.split("_")[1]
        res = generate_quater_report(request, q, y)
    elif(time=="annual"):
        #res = generate_annual_report(request, name)
        res = generate_quater_report(request, "none",name)
    elif(time=="staff" and name=="list"):
        res = generate_stafflist_report(request)
    elif(time=="audit" and name=="list"):
        res = generate_auditlist_report(request)
    return JsonResponse(res)

def report_json(request):
    departments = Department.objects.all()
    manPowerReport = []
    # ..manpower report..
    manpower = manpower_disposition(departments, manPowerReport)

    # ..

    staff_movement_summary_data = []
    staff_movement_summary(departments, staff_movement_summary_data)

    if request.POST:
        name =  request.POST.get('name')
        print name

    # ..disciplinary
    disciplinary_report_data = disciplinary_report()
    # ..staff_of_the_month
    staff_of_the_month_report_data = staff_of_the_month_report()
    # ..contract_apppointment
    contract_apppointment_report_data = contract_apppointment_report()
    # ..secondment
    secondment_report_data = secondment_report()
    # ..staff_disposition
    staff_disposition_report_data = staff_disposition_report()
    # ..change_of_name
    change_of_name_report_data = change_of_name_report()
    # ..change_of_nok
    change_of_nok_report_data = change_of_nok_report()
    # ..change_of_status
    change_of_status_report_data = change_of_status_report()
    # ..confirmation_of_appt
    confirmation_of_appt_report_data = confirmation_of_appt_report()
    # ..staff_movments
    staff_mov_report_data = staff_mov_report()
    # ..deployment
    deployment_report_data = deployment_report()
    # ..training
    training_report_data = training_report()
    # ..sick_leave
    sick_leave_report_data = sick_leave_report()
    # ..suspension
    suspension_report_data = suspension_report()
    # ..promotion
    promotion_report_data = promotion_report()
    # ..staff_exit
    staff_exit_report_data = staff_exit_report()
    # ..retirement
    retirement_report_data = retirement_report()

    #print staff_movement_summary_data
    """
    title = TableTitle.objects.get(title='DISCIPLINARY')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = TableData.objects.filter(table_id = str(title.pk))
    row = []
    for i in xrange(0,len(data),len(col)):
        row.append([])
        d=[]
        id_s = []
        for j in xrange(0, len(col)):
            d.append(data[i+j].data)
            id_s.append(data[i+j].id)
        row[-1].append(d)
        row[-1].append(id_s)

    title2 = TableTitle.objects.get(title='MONTHLY STAFF DISPOSITION')
    col = ColTitle.objects.filter(table_id = str(title2.pk))
    data = TableData.objects.filter(table_id = str(title2.pk))
    row2 = []
    for i in xrange(0,len(data),len(col)):
        row2.append([])
        for j in xrange(0, len(col)):
            row2[-1].append(data[i+j].data)


    print row2
    MONTHLY_STAFF_DISPOSITION = []
    for data in row2:
        vals = {}
        vals['name']=data[0]
        vals['rank']=data[1]
        vals['gl']=data[2]
        vals['dept']=data[3]
        vals['date']=data[4]
        vals['rfl']=data[5]

        MONTHLY_STAFF_DISPOSITION.append(vals)

        print MONTHLY_STAFF_DISPOSITION"""

    return JsonResponse({"manpower":manpower,
                         "dis":disciplinary_report_data,
                         "sotm":staff_of_the_month_report_data,
                         "cont_a":contract_apppointment_report_data,
                         "sec":secondment_report_data,
                         "sdis":staff_disposition_report_data,
                         "c_name":change_of_name_report_data,
                         "c_nok":change_of_nok_report_data,
                         "c_stat":change_of_status_report_data,
                         "conf_a":confirmation_of_appt_report_data,
                         "smov":staff_mov_report_data,
                         "depl":deployment_report_data,
                         "tra":training_report_data,
                         "sick":sick_leave_report_data,
                         "susp":suspension_report_data,
                         "prom":promotion_report_data,
                         "sexit":staff_exit_report_data,
                         "reti":retirement_report_data
                         })


#---------------------
def staff_list_report_gen(departments, manPowerReport, lastline):
    for department in departments:
        designation = []
        manPowerReport.append([])
        manPowerReport[-1].append(department.name)
        for i in xrange(3, 18):
            temp = str(Profile.objects.filter(department=department.name, pre_gl=str(i)).count())
            if department.name=="HUMAN RESOURCES":
                print temp
            if (temp == "0"):
                designation.append(" - ")
            else:
                #designation.append(" " + temp + " ")
                designation.append(temp)
                lastline[i - 1][0] = lastline[i - 1][0] + int(temp)

        manPowerReport[-1].append(designation)
        temp = str(Profile.objects.filter(department=department).count())
        if (temp == "0"):
            manPowerReport[-1].append(" - ")
        else:
            manPowerReport[-1].append(" " + temp + " ")

    lastline.append([Profile.objects.all().count()])


def staff_movement_summary(departments, staff_movement_summary_data):
    for department in departments:
        staffMovementSummaryReport = StaffMovementSummaryReport(department.name)
        junior = 0
        for i in xrange(3, 7):
            temp = str(Profile.objects.filter(department=department.name, designation=i).count())
            if (temp == "0"):
                pass
            else:
                junior += int(temp)

        senior = 0
        for i in xrange(7, 18):
            temp = str(Profile.objects.filter(department=department.name, designation=i).count())
            if (temp == "0"):
                pass
            else:
                senior += int(temp)
        total_staff = Profile.objects.filter(department=department.name).count()
        #num of promotion
        promotion_no = get_count("PROMOTION, ADVANCEMENT, UPGRADING & CONVERSION REGISTER", 1, department.name)
        disciplinary_cases = get_count("DISCIPLINARY", 1, department.name)
        suspention_cases = get_count("SUSPENSION/COMPULSORY LEAVE", 1, department.name)
        exit_cases = get_count("STAFF EXIT", 1, department.name)

        #disciplinary_cases = 6
        #Disciplinary.objects.filter(department=department.name).count()
        staffMovementSummaryReport.no_of_senior_staff = senior
        staffMovementSummaryReport.no_of_junior_staff = junior
        staffMovementSummaryReport.total_no_of_staff = total_staff
        staffMovementSummaryReport.disciplinary_cases = disciplinary_cases
        staffMovementSummaryReport.promotion_no = promotion_no
        staffMovementSummaryReport.suspention_cases = suspention_cases
        staffMovementSummaryReport.exit_cases = exit_cases

        # add objects to array

        staff_movement_summary_data.append(staffMovementSummaryReport)
        # Todo: add last line 'Total'

def monthly_training_matter(departments, monthly_training_matter_data):
    for department in departments:
        monthlyTrainingMatterReport = MonthlyTrainingMatterReport(department.name)
        total_staff = Profile.objects.filter(department=department.name).count()
        monthlyTrainingMatterReport.total_no_of_staff = total_staff

        study_leave = get_count("TRAINING MATTER", 1, department.name)
        monthlyTrainingMatterReport.study_leave = study_leave
        monthlyTrainingMatterReport.completion_of_study = study_leave

        nysc  = Nysc.objects.filter(department=department.name).count()
        siwes = Siwes.objects.filter(department=department.name).count()

        monthlyTrainingMatterReport.nysc  = nysc
        monthlyTrainingMatterReport.siwes = siwes

        monthly_training_matter_data.append(monthlyTrainingMatterReport)

def manpower(departments, manPowerReport, lastline):
    for department in departments:
        designation = []
        manPowerReport.append([])
        manPowerReport[-1].append(department.name)
        for i in xrange(3, 18):
            temp = str(Profile.objects.filter(department=department, designation=i).count())
            if (temp == "0"):
                designation.append(" - ")
            else:
                designation.append(" " + temp + " ")
                lastline[i - 1][0] = lastline[i - 1][0] + int(temp)

        manPowerReport[-1].append(designation)
        temp = str(Profile.objects.filter(department=department).count())
        if (temp == "0"):
            manPowerReport[-1].append(" - ")
        else:
            manPowerReport[-1].append(" " + temp + " ")

    lastline.append([Profile.objects.all().count()])

def get_count(title, pos, dept_name):
    if(len(TableTitle.objects.filter(title=title)) == 0):
        count = 0 
    else:
        title = TableTitle.objects.filter(title__contains=title)[0]
        col = ColTitle.objects.filter(table_id = str(title.pk))
        data = TableData.objects.filter(table_id = str(title.pk))
        count = 0
        row = []
        for i in xrange(0,len(data),len(col)):
            row.append([])
            d=[]
            id_s = []
            for j in xrange(0, len(col)):
                d.append(data[i+j].data)
                id_s.append(data[i+j].id)
            row[-1].append(d)
            row[-1].append(id_s)
        for r in row:
            if(r[0][1]==dept_name):
                count+=1
        
    return count

class Profile_template:
    def __init__(self, name, title,	sex, date_of_birth, staff_no, designation, gl, date_of_first_Appt, date_of_conf, date_of_last_promotion, lga, state_of_origin, department):
        self.name = name
        self.title = title
        self.sex = sex
        self.date_of_birth = date_of_birth
        self.staff_no = staff_no
        self.qualification_with_date = "kkk"
        self.designation = designation
        self.gl = gl
        self.date_of_first_Appt = date_of_first_Appt
        self.date_of_conf = date_of_conf
        self.date_of_last_promotion = date_of_last_promotion
        self.lga = lga
        self.state_of_origin = state_of_origin
        self.department = department
        self.id

    def set_qualification_with_date(self, qualification_with_date):
        self.qualification_with_date = qualification_with_date

def manpower_disposition(departments, manPowerReport):

    lastline = [
        [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]
    ]
    #manpower(departments, manPowerReport, lastline)
    staff_list_report_gen(departments, manPowerReport, lastline)
    ddd = []
    for m in manPowerReport:
        vals = {}
        vals['dept']=m[0]
        i=1
        for n in m[1]:
            vals[str(i)]=n
            i+=1
        emp_count = Profile.objects.filter(department=m[0]).count()
        vals[str(i)]=emp_count
        ddd.append(vals)
    vals = {}
    vals['dept']="TOTAL"
    i=1
    lastline.pop(0)
    lastline.pop(0)
    for n in lastline:
        vals[str(i)]=n
        i+=1
    emp_count = Profile.objects.all().count()
    vals[str(i)]=emp_count
    ddd.append(vals)

    return ddd

