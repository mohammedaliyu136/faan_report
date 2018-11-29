#from .models import Profile
from django.shortcuts import get_object_or_404

from employee.models import Profile, Department, AcademicProfessionalQualification
#from report.views import staff_list_report_gen
from report.models import TableTitle, ColTitle, TableData
import inflect


def update_employee(report_title, rep_data, emp_id):
    if("PROMOTION, ADVANCEMENT, UPGRADING & CONVERSION REGISTER"==str(report_title)):
        promotion(rep_data, emp_id)
    elif("CHANGE OF STATUS/ NOTIFICATION OF MARRIAGE"==str(report_title)):
        change_status(rep_data, emp_id)
    elif("CHANGE OF NEXT OF KIN"==str(report_title)):
        next_of_kin(rep_data, emp_id)
    elif("CHANGE OF NAME"==str(report_title)):
        change_name(rep_data, emp_id)
    elif("DEPLOYMENT/ INTER-DEPARTMENTAL TRANSFER"==str(report_title)):
        deployment(rep_data, emp_id)

def promotion(rep_data, emp_id):
    # 4,5 === gl,
    rank = str(rep_data[4][1])
    gl = str(rep_data[5][1])
    #print rank, gl, emp_id
    #obj = get_object_or_404(Profile, staff_no=emp_id)
    try:
        #obj = get_object_or_404(Profile, staff_no=emp_id)
        obj = Profile.objects.get(staff_no=emp_id)
        obj.gl = gl
        obj.save()
    except Profile.DoesNotExist:
        obj = "NONE"
    #print obj

    """
    gl
    """

def change_status(rep_data, emp_id):
    #status
    status = str(rep_data[3][1])
    #print status, emp_id
    try:
        #obj = get_object_or_404(Profile, staff_no=emp_id)
        obj = Profile.objects.get(staff_no=emp_id)
        obj.status = status
        obj.save()
    except Profile.DoesNotExist:
        obj = "NONE"
    #print obj

    """
    status
    """

def next_of_kin(rep_data, emp_id):
    # 3,4
    previous_nok = str(rep_data[2][1])
    current_nok = str(rep_data[3][1])
    relationship = str(rep_data[4][1])
    #print current_nok, relationship, emp_id
    #print rep_data
    try:
        #obj = get_object_or_404(Profile, staff_no=emp_id)
        obj = Profile.objects.get(staff_no=emp_id)
        if(obj.nok_name_1==previous_nok):
            obj.nok_name_1 = current_nok
        elif(obj.nok_name_2==previous_nok):
            obj.nok_name_2 = current_nok
        obj.save()
    except Profile.DoesNotExist:
        obj = "NONE"
    print obj

    """
    nok_name_1
    nok_address_1
    nok_relationship_1
    """

def change_name(rep_data, emp_id):
    names = rep_data[0][1].split(" ")
    #print names, emp_id
    #print rep_data
    if(len(names)>1):
        try:
            #obj = get_object_or_404(Profile, staff_no=emp_id)
            obj = Profile.objects.get(staff_no=emp_id)
            obj.surname = names[0]
            obj.othername = names[1]
            obj.save()
        except Profile.DoesNotExist:
            obj = "NONE"

    """
    surname
    othername
    maidenname
    """

def deployment(rep_data, emp_id):
    dept = str(rep_data[4][1])
    designation = str(rep_data[5][1])
    #print dept+"  "+designation+" "+emp_id
    try:
        obj = Profile.objects.get(staff_no=emp_id)
        obj.department = dept
        obj.designation = designation
        obj.save()
    except Profile.DoesNotExist:
        obj = "NONE"

    """
    department
    designation
    """

def monthly_data():
    pass

#--------------------------
#...hard data prep for json
#--------------------------
def get_data(title_id, month='none', quater='none', year='none'):
    #return TableData.objects.filter(table_id = str(title_id), year_d="2018")
    print quater, year
    if month != "none":
        #print month
        data = month.split("_")
        return TableData.objects.filter(table_id = str(title_id), month_d=data[0], year_d=data[1])
    elif quater != "none" and year != "none":
        return TableData.objects.filter(table_id = str(title_id), quater_d=quater, year_d=year)
    elif year != "none":
        return TableData.objects.filter(table_id = str(title_id), year_d=year)

def disciplinary_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='DISCIPLINARY')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    #data = TableData.objects.filter(table_id = str(title.pk), month_d=month)
    data = get_data(title.pk, month,quater, year)
    print "+++++++++++++++++++++"
    print quater, year
    print "+++++++++++++++++++++"
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['dept']  = data[i+1].data
        vals['rank']  = data[i+2].data
        vals['gl']  = data[i+3].data
        vals['date']  = data[i+4].data
        vals['offence']  = data[i+5].data
        vals['rem']  = data[i+6].data
        row.append(vals)
    return row

def staff_of_the_month_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='PARTICULAR OF STAFF EMPLOYMENT FOR THE MONTH')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['post']  = data[i+1].data
        vals['qualification']  = data[i+2].data
        vals['gl']  = data[i+3].data
        vals['date']  = data[i+4].data
        vals['dept_employed_to_work']  = data[i+5].data
        row.append(vals)
    print row
    return row


def contract_apppointment_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='CONTRACT APPOINTMENT')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['qualification']  = data[i+1].data
        vals['dept']  = data[i+2].data
        vals['date']  = data[i+3].data
        vals['remarks']  = data[i+4].data
        row.append(vals)
    return row

def secondment_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='SECONDMENT')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['gl']  = data[i+1].data
        vals['dept']  = data[i+2].data
        vals['date']  = data[i+3].data
        vals['station']  = data[i+4].data
        vals['remarks']  = data[i+5].data
        row.append(vals)
    return row


def staff_disposition_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='MONTHLY STAFF DISPOSITION')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['rank']  = data[i+1].data
        vals['gl']  = data[i+2].data
        vals['dept']  = data[i+3].data
        vals['date']  = data[i+4].data
        vals['rea']  = data[i+5].data
        row.append(vals)
    return row

def change_of_name_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='CHANGE OF NAME')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['rank']  = data[i+1].data
        vals['dept']  = data[i+2].data
        vals['pre_name']  = data[i+3].data
        vals['date']  = data[i+4].data
        vals['remarks']  = data[i+5].data
        row.append(vals)
    return row

def change_of_nok_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='CHANGE OF NEXT OF KIN')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['dept']  = data[i+1].data
        vals['pre_nok']  = data[i+2].data
        vals['cur_nok']  = data[i+3].data
        vals['relationship']  = data[i+4].data
        vals['date']  = data[i+5].data
        row.append(vals)
    return row


def change_of_status_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title="CHANGE OF STATUS/ NOTIFICATION OF MARRIAGE")
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['dept']  = data[i+1].data
        vals['gl']  = data[i+2].data
        vals['status']  = data[i+3].data
        vals['date']  = data[i+4].data
        row.append(vals)
    return row


def confirmation_of_appt_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='CONFIRMATION OF APPONTMENT')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['dept']  = data[i+1].data
        vals['gl']  = data[i+2].data
        vals['d_app']  = data[i+3].data
        vals['d_conf']  = data[i+4].data
        row.append(vals)
    return row

def staff_mov_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='STAFF MOVEMENT')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['desig']  = data[i+1].data
        vals['dept']  = data[i+2].data
        vals['d_pos']  = data[i+3].data
        vals['d_arr']  = data[i+4].data
        vals['n_pos']  = data[i+5].data
        vals['pre_s']  = data[i+6].data
        row.append(vals)
    return row

def deployment_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='DEPLOYMENT/ INTER-DEPARTMENTAL TRANSFER')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['pre_d']  = data[i+1].data
        vals['old_d']  = data[i+2].data
        vals['d_left']  = data[i+3].data
        vals['n_dept']  = data[i+4].data
        vals['n_desig']  = data[i+5].data
        vals['d_reptd']  = data[i+6].data
        vals['rem']  = data[i+7].data
        row.append(vals)
    return row


def training_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(id=19)
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['dept']  = data[i+1].data
        vals['gl']  = data[i+2].data
        vals['ci']  = data[i+3].data
        vals['s_year']  = data[i+4].data
        vals['e_year']  = data[i+5].data
        vals['rem']  = data[i+6].data
        row.append(vals)
    return row


def sick_leave_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='MATERNITY, ANNUAL, SICK, EXAM, COMPASSIONATE & CASUAL LEAVE & LEAVE OF ABSENCE')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['dept']  = data[i+1].data
        vals['month']  = data[i+2].data
        vals['date']  = data[i+3].data
        vals['resum']  = data[i+4].data
        row.append(vals)
    return row

def suspension_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='SUSPENSION/COMPULSORY LEAVE')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['dept']  = data[i+1].data
        vals['rank']  = data[i+2].data
        vals['gl']  = data[i+3].data
        vals['noo']  = data[i+4].data
        vals['pen']  = data[i+5].data
        vals['peri']  = data[i+6].data
        vals['rem']  = data[i+7].data
        row.append(vals)
    return row

def promotion_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='PROMOTION, ADVANCEMENT, UPGRADING & CONVERSION REGISTER')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['dept']  = data[i+1].data
        vals['pre_r']  = data[i+2].data
        vals['pre_gl']  = data[i+3].data
        vals['n_rank']  = data[i+4].data
        vals['n_gl']  = data[i+5].data
        vals['date']  = data[i+6].data
        vals['rem']  = data[i+7].data
        row.append(vals)
    return row


def staff_exit_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='STAFF EXIT')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['desig']  = data[i+1].data
        vals['dept']  = data[i+2].data
        vals['gl']  = data[i+3].data
        vals['date']  = data[i+4].data
        vals['rem']  = data[i+5].data
        row.append(vals)
    return row


def retirement_report(month="none",quater="none", year="none"):
    title = TableTitle.objects.get(title='RETIREMENT')
    col = ColTitle.objects.filter(table_id = str(title.pk))
    data = get_data(title.pk, month, quater, year)
    row = []
    counter = 0
    for i in xrange(0,len(data),len(col)):
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = data[i+0].data
        vals['desig']  = data[i+1].data
        vals['dept']  = data[i+2].data
        vals['gl']  = data[i+3].data
        vals['date']  = data[i+4].data
        vals['rem']  = data[i+5].data
        row.append(vals)
    return row

def resignation_termination_disengagement_dismissal_withdrawal_report(month="none",quater="none", year="none"):
    retirement = retirement_report(month,quater, year)
    disciplinary = disciplinary_report(month,quater, year)
    rows = []
    counter = 0
    for disci in disciplinary:
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = disci["name"]
        vals['dept']  = disci["dept"]
        vals['rank']  = disci["rank"]
        vals['gl']  = disci["gl"]
        vals['date']  = disci["date"]
        vals['offence']  = disci["offence"]
        vals['rem']  = disci["rem"]
        rows.append(vals)

    for retir in retirement:
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = retir["name"]
        vals['dept']  = retir["dept"]
        vals['rank']  = retir["desig"]
        vals['gl']  = retir["gl"]
        vals['date']  = retir["date"]
        vals['offence']  = ""
        vals['rem']  = retir["rem"]
        rows.append(vals)
    return rows

def leave_matters_report(month="none",quater="none", year="none"):
    training = training_report(month,quater, year)
    sick_leave = sick_leave_report(month,quater, year)
    #suspension = suspension_report(month,quater, year)
    rows = []
    counter = 0
    for tr in training:
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = tr["name"]
        vals['dept']  = tr["dept"]
        vals['month']  = ""
        vals['e_date']  = tr["s_year"]
        vals['r_date']  = tr["e_year"]
        rows.append(vals)

    for sick in sick_leave:
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = sick["name"]
        vals['dept']  = sick["dept"]
        vals['month']  = sick["month"]
        vals['e_date']  = sick["date"]
        vals['r_date']  = sick["resum"]
        rows.append(vals)
    """
    for sus in suspension:
        counter+=1
        vals = {}
        vals['sn']  = counter
        vals['name']  = retir["name"]
        vals['dept']  = retir["dept"]
        vals['rank']  = retir["desig"]
        vals['gl']  = retir["gl"]
        vals['date']  = retir["date"]
        vals['offence']  = ""
        vals['rem']  = retir["rem"]
        rows.append(vals)
    """
    return rows


def generate_monthly_report(request, month, manpower):
    # ..disciplinary
    disciplinary_report_data = disciplinary_report(month)
    # ..staff_of_the_month
    staff_of_the_month_report_data = staff_of_the_month_report(month)
    # ..contract_apppointment
    contract_apppointment_report_data = contract_apppointment_report(month)
    # ..secondment
    secondment_report_data = secondment_report(month)
    # ..staff_disposition
    staff_disposition_report_data = staff_disposition_report(month)
    # ..change_of_name
    change_of_name_report_data = change_of_name_report(month)
    # ..change_of_nok
    change_of_nok_report_data = change_of_nok_report(month)
    # ..change_of_status
    change_of_status_report_data = change_of_status_report(month)
    # ..confirmation_of_appt
    confirmation_of_appt_report_data = confirmation_of_appt_report(month)
    # ..staff_movments
    staff_mov_report_data = staff_mov_report(month)
    # ..deployment
    deployment_report_data = deployment_report(month)
    # ..training
    training_report_data = training_report(month)
    # ..sick_leave
    sick_leave_report_data = sick_leave_report(month)
    # ..suspension
    suspension_report_data = suspension_report(month)
    # ..promotion
    promotion_report_data = promotion_report(month)
    # ..staff_exit
    staff_exit_report_data = staff_exit_report(month)
    # ..retirement
    retirement_report_data = retirement_report(month)

    print

    report ={"manpower":manpower,
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
             "reti":retirement_report_data,
             "month":month.split("_")[0],
             "year":month.split("_")[1],
             }
    return report

def generate_quater_report(request, quater, year):
    inf = inflect.engine()
    # ..staff strenght
    total_num_of_staff = Profile.objects.all().count()
    num_of_senior_staff = Profile.objects.filter(pre_gl__range=[7,18]).count()
    num_of_junior_staff = Profile.objects.filter(pre_gl__range=[1,7]).count()
    staff_strenght = {}
    staff_strenght["num_of_junior_staff"] = num_of_junior_staff
    staff_strenght["num_of_senior_staff"] = num_of_senior_staff
    staff_strenght["total_num_of_staff"] = total_num_of_staff


    # ..change_of_name
    change_of_name_report_data = change_of_name_report("none", quater, year)
    change_of_name_report_count = len(change_of_name_report_data)
    if change_of_name_report_count>0:
        change_of_name = {}
        change_of_name["is_empty"] = False
        change_of_name["not_empty"] = True
        change_of_name["data"] = change_of_name_report_data
        change_of_name["num_of_employee"] = change_of_name_report_count
        change_of_name["num_of_employee_str"] = inf.number_to_words(change_of_name_report_count).upper()
    else:
        change_of_name = {}
        change_of_name["is_empty"] = True
        change_of_name["not_empty"] = False


    # ..change_of_nok
    change_of_nok_report_data = change_of_nok_report("none", quater, year)
    change_of_nok_report_count = len(change_of_nok_report_data)
    if change_of_nok_report_count>0:
        change_of_nok = {}
        change_of_nok["is_empty"] = False
        change_of_nok["not_empty"] = True
        change_of_nok["data"] = change_of_nok_report_data
        change_of_nok["num_of_employee"] = change_of_nok_report_count
        change_of_nok["num_of_employee_str"] = inf.number_to_words(change_of_nok_report_count).upper()
    else:
        change_of_nok = {}
        change_of_nok["is_empty"] = True
        change_of_nok["not_empty"] = False


    # ..change_of_status
    change_of_status_report_data = change_of_status_report("none", quater, year)
    change_of_status_report_count = len(change_of_status_report_data)
    if change_of_status_report_count>0:
        change_of_status = {}
        change_of_status["is_empty"] = False
        change_of_status["not_empty"] = True
        change_of_status["data"] = change_of_status_report_data
        change_of_status["num_of_employee"] = change_of_status_report_count
        change_of_status["num_of_employee_str"] = (inf.number_to_words(change_of_status_report_count)).upper()
    else:
        change_of_status = {}
        change_of_status["is_empty"] = True
        change_of_status["not_empty"] = False

    # ..confirmation_of_appt_report
    confirmation_of_appt_report_data = confirmation_of_appt_report("none", quater, year)
    confirmation_of_appt_report_count = len(confirmation_of_appt_report_data)
    if confirmation_of_appt_report_count>0:
        confirmation_of_appt = {}
        confirmation_of_appt["is_empty"] = False
        confirmation_of_appt["not_empty"] = True
        confirmation_of_appt["data"] = confirmation_of_appt_report_data
        confirmation_of_appt["num_of_employee"] = confirmation_of_appt_report_count
        confirmation_of_appt["num_of_employee_str"] = inf.number_to_words(confirmation_of_appt_report_count).upper()
    else:
        confirmation_of_appt = {}
        confirmation_of_appt["is_empty"] = True
        confirmation_of_appt["not_empty"] = False


    # ..promotion_report
    promotion_report_data = promotion_report("none", quater, year)
    promotion_report_count = len(promotion_report_data)
    if promotion_report_count>0:
        promotion = {}
        promotion["is_empty"] = False
        promotion["not_empty"] = True
        promotion["data"] = promotion_report_data
        promotion["num_of_employee"] = promotion_report_count
        promotion["num_of_employee_str"] = inf.number_to_words(promotion_report_count).upper()

        promotion["total_p"] = get_total_promotion(promotion_report_data, "Promotion", "all")
        promotion["p_sen"] = get_total_promotion(promotion_report_data, "Promotion", "sen")
        promotion["p_jun"] = get_total_promotion(promotion_report_data, "Promotion", "jun")

        promotion["total_upgraded"] = get_total_promotion(promotion_report_data, "Upgrade", "all")
        promotion["upgraded_sen"] = get_total_promotion(promotion_report_data, "Upgrade", "sen")
        promotion["upgraded_jun"] = get_total_promotion(promotion_report_data, "Upgrade", "jun")

        promotion["total_converted"] = get_total_promotion(promotion_report_data, "Converted", "all")
        promotion["converted_sen"] = get_total_promotion(promotion_report_data, "Converted", "sen")
        promotion["converted_jun"] = get_total_promotion(promotion_report_data, "Converted", "jun")

        promotion["total_converted_and_upgraded"] = get_total_promotion(promotion_report_data, "Conversion/Promotion", "all")
        promotion["converted_and_upgraded_sen"] = get_total_promotion(promotion_report_data, "Conversion/Promotion", "sen")
        promotion["converted_and_upgraded_jun"] = get_total_promotion(promotion_report_data, "Conversion/Promotion", "jun")

        promotion["total_advancement"] = get_total_promotion(promotion_report_data, "Advancement", "all")
        promotion["advancement_sen"] = get_total_promotion(promotion_report_data, "Advancement", "sen")
        promotion["advancement_jun"] = get_total_promotion(promotion_report_data, "Advancement", "jun")

        promotion["total_re_designation"] = get_total_promotion(promotion_report_data, "Re-designation", "all")
        promotion["re_designation_sen"] = get_total_promotion(promotion_report_data, "Re-designation", "sen")
        promotion["re_designation_jun"] = get_total_promotion(promotion_report_data, "Re-designation", "jun")
    else:
        promotion = {}
        promotion["is_empty"] = True
        promotion["not_empty"] = False

    # ..contract_apppointment_report
    contract_apppointment_report_data = contract_apppointment_report("none", quater, year)
    contract_apppointment_report_count = len(contract_apppointment_report_data)
    if contract_apppointment_report_count>0:
        contract_apppointment = {}
        contract_apppointment["is_empty"] = False
        contract_apppointment["not_empty"] = True
        contract_apppointment["data"] = contract_apppointment_report_data
        contract_apppointment["num_of_employee"] = contract_apppointment_report_count
        contract_apppointment["num_of_employee_str"] = inf.number_to_words(contract_apppointment_report_count).upper()
    else:
        contract_apppointment = {}
        contract_apppointment["is_empty"] = True
        contract_apppointment["not_empty"] = False

    # ..secondment_report
    secondment_report_data = secondment_report("none", quater, year)
    secondment_report_count = len(secondment_report_data)
    if secondment_report_count>0:
        secondment = {}
        secondment["is_empty"] = False
        secondment["not_empty"] = True
        secondment["data"] = secondment_report_data
        secondment["num_of_employee"] = secondment_report_count
        secondment["num_of_employee_str"] = inf.number_to_words(secondment_report_count).upper()
    else:
        secondment = {}
        secondment["is_empty"] = True
        secondment["not_empty"] = False

    # ..deployment_report
    deployment_report_data = deployment_report("none", quater, year)
    deployment_report_count = len(deployment_report_data)
    if deployment_report_count>0:
        deployment = {}
        deployment["is_empty"] = False
        deployment["not_empty"] = True
        deployment["data"] = deployment_report_data
        deployment["num_of_employee"] = deployment_report_count
        deployment["num_of_employee_str"] = inf.number_to_words(deployment_report_count).upper()
    else:
        deployment = {}
        deployment["is_empty"] = True
        deployment["not_empty"] = False


    # ..training_report
    training_report_data = training_report("none", quater, year)
    training_report_count = len(training_report_data)
    if training_report_count>0:
        training = {}
        training["is_empty"] = False
        training["not_empty"] = True
        training["data"] = training_report_data
        training["num_of_employee"] = training_report_count
        training["num_of_employee_str"] = inf.number_to_words(training_report_count).upper()
    else:
        training = {}
        training["is_empty"] = True
        training["not_empty"] = False

    # ..disciplinary_report
    disciplinary_report_data = disciplinary_report("none", quater, year)
    disciplinary_report_count = len(disciplinary_report_data)
    if disciplinary_report_count>0:
        disciplinary = {}
        disciplinary["is_empty"] = False
        disciplinary["not_empty"] = True
        disciplinary["data"] = disciplinary_report_data
        disciplinary["num_of_employee"] = disciplinary_report_count
        disciplinary["num_of_employee_str"] = inf.number_to_words(disciplinary_report_count).upper()
    else:
        disciplinary = {}
        disciplinary["is_empty"] = True
        disciplinary["not_empty"] = False


    # ..retirement_report
    retirement_report_data = retirement_report("none", quater, year)
    retirement_report_count = len(retirement_report_data)
    if retirement_report_count>0:
        retirement = {}
        retirement["is_empty"] = False
        retirement["not_empty"] = True
        retirement["data"] = retirement_report_data
        retirement["num_of_employee"] = retirement_report_count
        retirement["num_of_employee_str"] = inf.number_to_words(retirement_report_count).upper()
    else:
        retirement = {}
        retirement["is_empty"] = True
        retirement["not_empty"] = False


    # ..staff_exit_report
    staff_exit_report_data = staff_exit_report("none", quater, year)
    staff_exit_report_count = len(staff_exit_report_data)
    if staff_exit_report_count>0:
        staff_exit = {}
        staff_exit["is_empty"] = False
        staff_exit["not_empty"] = True
        staff_exit["data"] = staff_exit_report_data
        staff_exit["num_of_employee"] = staff_exit_report_count
        staff_exit["num_of_employee_str"] = inf.number_to_words(staff_exit_report_count).upper()
    else:
        staff_exit = {}
        staff_exit["is_empty"] = True
        staff_exit["not_empty"] = False

    # ..staff_movement_report leave_matters_report
    staff_mov_report_data = staff_mov_report("none", quater, year)
    staff_mov_report_count = len(staff_mov_report_data)
    if staff_mov_report_count>0:
        staff_mov = {}
        staff_mov["is_empty"] = False
        staff_mov["not_empty"] = True
        staff_mov["data"] = staff_mov_report_data
        staff_mov["num_of_employee"] = staff_mov_report_count
        staff_mov["num_of_employee_str"] = inf.number_to_words(staff_mov_report_count).upper()
    else:
        staff_mov = {}
        staff_mov["is_empty"] = True
        staff_mov["not_empty"] = False
    #..resignation_termination_disengagement_dismissal_withdrawal_report
    resignation_termination_disengagement_dismissal_withdrawal_report_data = resignation_termination_disengagement_dismissal_withdrawal_report(month="none",quater=quater, year=year)
    resignation_termination_disengagement_dismissal_withdrawal_report_count = len(resignation_termination_disengagement_dismissal_withdrawal_report_data)
    if resignation_termination_disengagement_dismissal_withdrawal_report_count>0:
        resignation_termination_disengagement_dismissal_withdrawal = {}
        resignation_termination_disengagement_dismissal_withdrawal["is_empty"] = False
        resignation_termination_disengagement_dismissal_withdrawal["not_empty"] = True
        resignation_termination_disengagement_dismissal_withdrawal["data"] = resignation_termination_disengagement_dismissal_withdrawal_report_data
        resignation_termination_disengagement_dismissal_withdrawal["num_of_employee"] = resignation_termination_disengagement_dismissal_withdrawal_report_count
        resignation_termination_disengagement_dismissal_withdrawal["num_of_employee_str"] = inf.number_to_words(resignation_termination_disengagement_dismissal_withdrawal_report_count).upper()
    else:
        resignation_termination_disengagement_dismissal_withdrawal = {}
        resignation_termination_disengagement_dismissal_withdrawal["is_empty"] = True
        resignation_termination_disengagement_dismissal_withdrawal["not_empty"] = False

    #..leave_matters_report
    leave_matters_report_data = leave_matters_report(month="none",quater=quater, year=year)
    leave_matters_report_count = len(leave_matters_report_data)
    if leave_matters_report_count>0:
        leave_matters = {}
        leave_matters["is_empty"] = False
        leave_matters["not_empty"] = True
        leave_matters["data"] = leave_matters_report_data
        leave_matters["num_of_employee"] = leave_matters_report_count
        leave_matters["num_of_employee_str"] = inf.number_to_words(leave_matters_report_count).upper()
    else:
        leave_matters = {}
        leave_matters["is_empty"] = True
        leave_matters["not_empty"] = False


    # ..staff_of_the_month_report ++++++++++++++++++++++++*************
    staff_of_the_month_report_data = staff_of_the_month_report("none", quater, year)
    staff_of_the_month_report_count = len(staff_of_the_month_report_data)
    senior_no_employees = 0
    junior_no_employees = 0
    for st in staff_of_the_month_report_data:
        gl_step = st["gl"]
        try:
            gl = int(gl_step.split("/")[0])
            if gl in xrange(3, 7):
                junior_no_employees+=1
                print True
            elif gl in xrange(7, 18):
                senior_no_employees+=1
                print False
        except:
            pass

    if staff_of_the_month_report_count>0:
        staff_of_the_month = {}
        staff_of_the_month["is_empty"] = False
        staff_of_the_month["not_empty"] = True
        staff_of_the_month["data"] = staff_of_the_month_report_data
        staff_of_the_month["num_of_employee"] = staff_of_the_month_report_count
        staff_of_the_month["num_of_employee_str"] = inf.number_to_words(staff_of_the_month_report_count).upper()
        staff_of_the_month["senior_no_employees"] = senior_no_employees,
        staff_of_the_month["senior_no_employees_str"] = inf.number_to_words(senior_no_employees).upper(),
        staff_of_the_month["junior_no_employees"] = junior_no_employees,
        staff_of_the_month["junior_no_employees_str"] = inf.number_to_words(junior_no_employees).upper(),
    else:
        staff_of_the_month = {}
        staff_of_the_month["is_empty"] = True
        staff_of_the_month["not_empty"] = False


    if quater == "none":
        report_title = "ANNUAL REPORTS "+str(year)
        report_date = "31 December, "+str(year)
    else:
        if quater == "Q1":
            report_title = "FIRST QUARTER REPORTS (JANUARY - MARCH, "+year+")"
            report_date = "31 March, "+str(year)
        elif quater == "Q2":
            report_title = "SECOND QUARTER REPORTS (APRIL - JUNE, "+year+")"
            report_date = "30 June, "+str(year)
        elif quater == "Q3":
            report_title = "THIRD QUARTER REPORTS (JULY - SEPTEMBER, "+year+")"
            report_date = "31 September, "+str(year)
        elif quater == "Q4":
            report_title = "FOURTH QUARTER REPORTS (OCTOBER - DECEMBER, "+year+")"
            report_date = "31 December, "+str(year)

    staff_exit_total = staff_exit_report_count+retirement_report_count
    if staff_exit_total == 0:
        staff_exit_total = "No"
    print "------------------"
    staff_exit_total = inf.number_to_words(staff_exit_total).upper() + " ("+str(staff_exit_total)+")"

    report ={
             "report_title":report_title,
             "report_date":report_date,
             "num_of_junior_staff":num_of_junior_staff,
             "num_of_senior_staff":num_of_senior_staff,
             "total_num_of_staff":total_num_of_staff,
             "c_name":[change_of_name],
             "change_of_nok":[change_of_nok],
             "change_of_status":[change_of_status],
             "conf_of_appt":[confirmation_of_appt],
             "promotion":[promotion],
             "con_appt":[contract_apppointment],
             "secondment":[secondment],
             "inter_dept_transfer":[deployment],
             "training":[training],
             "dis":[disciplinary],
             "staff_exit_total":staff_exit_total,
             "retirement":[retirement],
             "staff_exit":[staff_exit],
             "resignation":[resignation_termination_disengagement_dismissal_withdrawal],
             "leave_matter":[leave_matters],

             "total_no_recruited":staff_of_the_month,
             #"total_no_recruited":[{"num_of_employee": 34,
             #                       "num_of_employee_str": inf.number_to_words(34).upper(),
             #                       "is_empty":False,
             #                       "senior_no_employees":12,
             #                       "senior_no_employees_str":inf.number_to_words(12).upper(),
             #                       "junior_no_employees":22,
             #                       "junior_no_employees_str":inf.number_to_words(22).upper(),
             #                       "not_empty":True,
             #                       "data":[{"sn":1, "post":"nnnn"}]}],
             "staff_posted_in_and_out":staff_mov
             #"staff_posted_in_and_out":[{"num_of_employee": 34,
             #                            "num_of_employee_str": inf.number_to_words(34).upper(),
             #                            "is_empty":False,
             #                            "staff_posted_in":12,
             #                            "staff_posted_in_str":inf.number_to_words(12).upper(),
             #                            "staff_posted_out":22,
             #                            "staff_posted_out_str":inf.number_to_words(22).upper(),
             #                            "not_empty":True,
             #                            "data":[{"sn":1, "name":"nnnn"}]}]
             }
    return report
    """
    return {}
    """


def generate_annual_report(request, year):
    # ..staff strenght
    total_num_of_staff = Profile.objects.all().count()
    num_of_senior_staff = Profile.objects.filter(pre_gl__range=[7,18]).count()
    num_of_junior_staff = Profile.objects.filter(pre_gl__range=[1,7]).count()
    staff_strenght = {}
    staff_strenght["num_of_junior_staff"] = num_of_junior_staff
    staff_strenght["num_of_senior_staff"] = num_of_senior_staff
    staff_strenght["total_num_of_staff"] = total_num_of_staff
    staff_strenght = [staff_strenght]


    # ..change_of_name
    change_of_name_report_data = change_of_name_report("none", "none", year)
    change_of_name_report_count = len(change_of_name_report_data)
    if change_of_name_report_count>0:
        change_of_name = {}
        change_of_name["is_empty"] = False
        change_of_name["not_empty"] = True
        change_of_name["data"] = change_of_name_report_data
        change_of_name["num_of_employee"] = change_of_name_report_count
    else:
        change_of_name = {}
        change_of_name["is_empty"] = True
        change_of_name["not_empty"] = False


    # ..change_of_nok
    change_of_nok_report_data = change_of_nok_report("none", "none", year)
    change_of_nok_report_count = len(change_of_nok_report_data)
    if change_of_nok_report_count>0:
        change_of_nok = {}
        change_of_nok["is_empty"] = False
        change_of_nok["not_empty"] = True
        change_of_nok["data"] = change_of_nok_report_data
        change_of_nok["num_of_employee"] = change_of_nok_report_count
    else:
        change_of_nok = {}
        change_of_nok["is_empty"] = True
        change_of_nok["not_empty"] = False


    # ..change_of_status
    change_of_status_report_data = change_of_status_report("none", "none", year)
    change_of_status_report_count = len(change_of_status_report_data)
    if change_of_status_report_count>0:
        change_of_status = {}
        change_of_status["is_empty"] = False
        change_of_status["not_empty"] = True
        change_of_status["data"] = change_of_status_report_data
        change_of_status["num_of_employee"] = change_of_status_report_count
    else:
        change_of_status = {}
        change_of_status["is_empty"] = True
        change_of_status["not_empty"] = False

    # ..confirmation_of_appt_report
    confirmation_of_appt_report_data = confirmation_of_appt_report("none", "none", year)
    confirmation_of_appt_report_count = len(confirmation_of_appt_report_data)
    if confirmation_of_appt_report_count>0:
        confirmation_of_appt = {}
        confirmation_of_appt["is_empty"] = False
        confirmation_of_appt["not_empty"] = True
        confirmation_of_appt["data"] = confirmation_of_appt_report_data
        confirmation_of_appt["num_of_employee"] = confirmation_of_appt_report_count
    else:
        confirmation_of_appt = {}
        confirmation_of_appt["is_empty"] = True
        confirmation_of_appt["not_empty"] = False


    # ..promotion_report
    promotion_report_data = promotion_report("none", "none", year)
    promotion_report_count = len(promotion_report_data)
    if promotion_report_count>0:
        promotion = {}
        promotion["is_empty"] = False
        promotion["not_empty"] = True
        promotion["data"] = promotion_report_data
        promotion["num_of_employee"] = promotion_report_count
    else:
        promotion = {}
        promotion["is_empty"] = True
        promotion["not_empty"] = False




    report ={
             "staff_strenght":staff_strenght,
             "c_name":change_of_name,
             "change_of_nok":change_of_nok,
             "change_of_status":change_of_status,
             "conf_of_appt":confirmation_of_appt,
             "promotion":promotion
             }
    return report

def generate_stafflist_report(request):
    depts = Department.objects.all()
    row = []
    for dept in depts:
        profiles = Profile.objects.filter(department=dept.name)
        dddd = []
        gls = [18,17,16,15,14,13,12,11,10,"09","08","07","06","05","04","03","02","01"]
        for gl in gls:
            for p in profiles:
                if p.gl.split("/")[0]==gl:
                    dddd.append(p)
        profiles=dddd

        r = []
        d = {}
        counter = 0
        for profile in profiles:
            counter+=1
            vals = {}
            vals['sn']  = counter
            vals['name']  = profile.surname + " " + profile.othername + " " + profile.maidenname
            vals['state']  = profile.state
            vals['desig']  = profile.designation
            vals['title']  = profile.title
            vals['gender']  = profile.gender
            vals['date_of_birth']  = profile.date_of_birth
            vals['staff_no']  = profile.staff_no
            vals['gl']  = profile.gl
            vals['date_of_first_appt']  = profile.date_of_first_Appt
            vals['date_of_conf']  = profile.date_of_conf
            vals['lga']  = profile.lga
            vals['date_of_last_promotion']  = profile.date_of_last_promotion

            academicProfessionalQualification = AcademicProfessionalQualification.objects.filter(profile_id=profile.id)
            qu = []
            for apq in academicProfessionalQualification:
                qu_val={}
                qu_val["name"] = apq.name
                qu_val["date"] = apq.date
                qu.append(qu_val)
            vals['qualification']  = qu



            r.append(vals)
        d['dept_data'] = r
        d['dept'] = dept.name
        row.append(d)
    report ={
             "stafflist":row,
             #"dept":depts
    }
    return report


def generate_auditlist_report(request):
    depts = Department.objects.all().order_by('name')
    audit_dept = Department.objects.get(id=6)
    dept_tem = []
    dept_tem.append(audit_dept)
    for d in depts:
        if d.name==audit_dept.name:
            pass
        else:
            dept_tem.append(d)
    depts=dept_tem
    row = []
    for dept in depts:

        profiles = Profile.objects.filter(department=dept.name)
        dddd = []
        gls = [18,17,16,15,14,13,12,11,10,"09","08","07","06","05","04","03","02","01"]
        for gl in gls:
            for p in profiles:
                if p.gl.split("/")[0]==str(gl):
                    dddd.append(p)
        profiles=dddd



        r = []
        d = {}
        counter = 0
        for profile in profiles:
            counter+=1
            vals = {}
            vals['sn']  = counter
            vals['staff_no_acct']  = profile.staff_no
            vals['name']  = profile.surname + " " + profile.othername + " " + profile.maidenname
            vals['designation']  = profile.designation
            vals['gl']  = profile.gl
            #vals['department']  = profile.department
            vals['department']  = " '' "
            if profile.occupant:
                vals['occupant']  = "QUARTERED"
            else:
                vals['occupant']  = "NOT QUARTERED"
            vals['status']  = profile.status
            vals['remark']  = ''


            r.append(vals)
        d['dept_data'] = r
        d['dept'] = dept.name
        row.append(d)

    #p = Profile.objects.filter(department__in=depts)
    #

    report ={
             "auditlist":row,
             #"dept":depts
             "Kitty":"jdhdjjd",
             "hasKitty": ""
    }
    return report

def get_total_promotion(data, remark, gl):
    counter=0
    if "all"==gl:
        for d in data:
            if d["rem"]==remark:
                counter+=1
    elif "sen"==gl:
        for d in data:
            if d["rem"]==remark and int(d["n_gl"].split("/")[0]) in [7,8,9,10,11,12,13,14,15,16,17]:
                counter+=1
    elif "jun"==gl:
        for d in data:
            if d["rem"]==remark and int(d["n_gl"].split("/")[0]) in [1,2,3,4,5,6,]:
                counter+=1
    return counter
