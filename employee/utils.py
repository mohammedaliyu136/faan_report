import datetime

from report.models import TableTitle, ColTitle, TableData
from .models import Department, Designation, Profile, EducationInstitutions, AcademicProfessionalQualification

def save_educational_instition_attended(ed_institution_ids, request, profile_id):
    print "save_educational_instition_attended"
    print request.POST.get('staff_no')

    ed_institution_ids = ed_institution_ids.split(",")
    print ed_institution_ids
    for i in ed_institution_ids:
        name      = request.POST.get('ed_institution_name_'+i)
        address   = request.POST.get('ed_institution_address_'+i)
        from_date = request.POST.get('ed_institution_from_'+i)
        to_date   = request.POST.get('ed_institution_to_'+i)

        EducationInstitutions(profile_id=profile_id, name=name, address=address, from_date=from_date, to_date=to_date).save()

def save_academic_professional_qualification(academic_form_ids, request, profile_id):
    print "save_educational_instition_attended"
    print request.POST.get('staff_no')

    academic_form_ids = academic_form_ids.split(",")
    print academic_form_ids
    for i in academic_form_ids:
        name = request.POST.get('academic_name_'+i)
        date = request.POST.get('academic_date_'+i)
        AcademicProfessionalQualification(profile_id=profile_id, name = name, date=date).save()

def save_profile(request):
    title          = request.POST.get('title')
    surname        = request.POST.get('surname')
    other_name     = request.POST.get('other_name')
    maiden_name    = request.POST.get('maiden_name')
    state_origin   = request.POST.get('state_origin')
    lga            = request.POST.get('lga')
    date_of_birth  = request.POST.get('date_of_birth')
    place_of_birth = request.POST.get('place_of_birth')
    marital_status = request.POST.get('marital_status')
    gender         = request.POST.get('gender')
    name_of_spouse = request.POST.get('spouse_name')
    department     = request.POST.get('department')
    occupant     = request.POST.get('occupant')

    nok_name_1    = request.POST.get('nok_name_1')
    nok_address_1 = request.POST.get('nok_address_1')
    nok_relationship_1 = request.POST.get('nok_relationship_1')
    nok_name_2    = request.POST.get('nok_name_2')
    nok_address_2 = request.POST.get('nok_address_2')
    nok_relationship_2 = request.POST.get('nok_relationship_2')

    

    date_first_appt      = request.POST.get('date_first_appt')
    designation          = request.POST.get('designation')
    salary_grade_level   = request.POST.get('salary_grade_level')
    date_of_confirmation = request.POST.get('date_of_confirmation')
    name_of_employer     = request.POST.get('name_of_employer')
    date_of_transfer     = request.POST.get('date_of_transfer')
    #rank                 = request.POST.get('rank')
    grade_level          = request.POST.get('salary_grade_level')
    gl_step              = grade_level.split("/")[0]
    grade_lepresent_salaryvel = request.POST.get('present_salary')
    last_promotion       = request.POST.get('last_promotion')
    staff_no             = request.POST.get('staff_no')
    account_num          = ""

    #..................................................
    new_recruite             = request.POST.get('new_recruite')
    if new_recruite=="yes":
        date_posting    =   request.POST.get('date_of_posting')
        date_of_arrival    =   request.POST.get('date_of_arrival')
        new_posting    =   request.POST.get('new_posting')
        previous_station    =   request.POST.get('previous_station')

        val = {}
        val["name"] = surname +" "+ other_name +" "+ maiden_name
        val["designation"] = designation
        val["department"] = department
        val["date_of_posting"] = date_posting
        val["date_of_arrival"] = date_of_arrival
        val["new_posting"] = new_posting
        val["previous_station"] = previous_station

        title = TableTitle.objects.get(title="STAFF MOVEMENT")
        col = ColTitle.objects.filter(table_id = str(title.pk))
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

        TableData(col_id=col[0].id, data=val["name"], table_id=title.id, month_d = mon, quater_d = quater_str, year_d = myear).save()
        TableData(col_id=col[1].id, data=designation, table_id=title.id, month_d = mon, quater_d = quater_str, year_d = myear).save()
        TableData(col_id=col[2].id, data=department, table_id=title.id, month_d = mon, quater_d = quater_str, year_d = myear).save()
        TableData(col_id=col[3].id, data=date_posting, table_id=title.id, month_d = mon, quater_d = quater_str, year_d = myear).save()
        TableData(col_id=col[4].id, data=date_of_arrival, table_id=title.id, month_d = mon, quater_d = quater_str, year_d = myear).save()
        TableData(col_id=col[5].id, data=new_posting, table_id=title.id, month_d = mon, quater_d = quater_str, year_d = myear).save()
        TableData(col_id=col[6].id, data=previous_station, table_id=title.id, month_d = mon, quater_d = quater_str, year_d = myear).save()


    profile = Profile(title=title, surname=surname, othername=other_name, maidenname=maiden_name, spouse_name=name_of_spouse, gender=gender,date_of_birth=date_of_birth, homeplace=place_of_birth, lga=lga, state=state_origin, country="country", status=marital_status, designation=designation, gl=grade_level, department=department, date_of_first_Appt=date_first_appt, date_of_conf=date_of_confirmation, name_employer=name_of_employer, date_of_transfer=date_of_transfer, pre_gl=gl_step, pre_salary=salary_grade_level, date_of_last_promotion=last_promotion, staff_no=staff_no, occupant=occupant, nok_name_1=nok_name_1, nok_address_1=nok_address_1, nok_relationship_1=nok_relationship_1, nok_name_2=nok_name_2, nok_address_2=nok_address_2, nok_relationship_2=nok_relationship_2, account_num=account_num)
    profile.save()
    return profile.id

# ****************** update **********************
def update_educational_instition_attended(ed_institution_ids, request, profile_id):
    print "save_educational_instition_attended"
    print request.POST.get('staff_no')

    ed_institution_ids = ed_institution_ids.split(",")
    print ed_institution_ids
    EducationInstitutions.objects.filter(profile_id=profile_id).delete()
    for i in ed_institution_ids:
        name      = request.POST.get('ed_institution_name_'+i)
        address   = request.POST.get('ed_institution_address_'+i)
        from_date = request.POST.get('ed_institution_from_'+i)
        to_date   = request.POST.get('ed_institution_to_'+i)
        
        EducationInstitutions(profile_id=profile_id, name=name, address=address, from_date=from_date, to_date=to_date).save()

def update_academic_professional_qualification(academic_form_ids, request, profile_id):
    print "save_educational_instition_attended"
    print request.POST.get('staff_no')
    AcademicProfessionalQualification.objects.filter(profile_id=profile_id).delete()
    academic_form_ids = academic_form_ids.split(",")
    print academic_form_ids
    for i in academic_form_ids:
        name = request.POST.get('academic_name_'+i)
        date = request.POST.get('academic_date_'+i)
        AcademicProfessionalQualification(profile_id=profile_id, name = name, date=date).save()

def update_profile(request, profile_id):
    title          = request.POST.get('title')
    surname        = request.POST.get('surname')
    other_name     = request.POST.get('other_name')
    maiden_name    = request.POST.get('maiden_name')
    state_origin   = request.POST.get('state_origin')
    lga            = request.POST.get('lga')
    date_of_birth  = request.POST.get('date_of_birth')
    place_of_birth = request.POST.get('place_of_birth')
    marital_status = request.POST.get('marital_status')
    gender         = request.POST.get('gender')
    name_of_spouse = request.POST.get('spouse_name')
    department     = request.POST.get('department')
    occupant       = request.POST.get('occupant')
    if occupant == "True":
        occupant = True
    else:
        occupant = False

    nok_name_1    = request.POST.get('nok_name_1')
    nok_address_1 = request.POST.get('nok_address_1')
    nok_relationship_1 = request.POST.get('nok_relationship_1')
    nok_name_2    = request.POST.get('nok_name_2')
    nok_address_2 = request.POST.get('nok_address_2')
    nok_relationship_2 = request.POST.get('nok_relationship_2')

    

    date_first_appt      = request.POST.get('date_first_appt')
    designation          = request.POST.get('designation')
    salary_grade_level   = request.POST.get('salary_grade_level')
    date_of_confirmation = request.POST.get('date_of_confirmation')
    name_of_employer     = request.POST.get('name_of_employer')
    date_of_transfer     = request.POST.get('date_of_transfer')
    rank                 = request.POST.get('rank')
    grade_level          = request.POST.get('salary_grade_level')
    grade_lepresent_salaryvel = request.POST.get('present_salary')
    last_promotion       = request.POST.get('last_promotion')
    staff_no             = request.POST.get('staff_no')
    account_num          = request.POST.get('account_num')

    profile = Profile.objects.get(id=profile_id)
    profile.title=title 
    profile.surname=surname
    profile.othername=other_name 
    profile.maidenname=maiden_name 
    profile.spouse_name=name_of_spouse 
    profile.gender=gender
    profile.date_of_birth=date_of_birth 
    profile.homeplace=place_of_birth 
    profile.lga=lga 
    profile.state=state_origin 
    profile.country="country" 
    profile.status=marital_status 
    profile.designation=designation 
    profile.gl=grade_level 
    profile.department=department 
    profile.date_of_first_Appt=date_first_appt 
    profile.date_of_conf=date_of_confirmation 
    profile.name_employer=name_of_employer 
    profile.date_of_transfer=date_of_transfer 
    #profile.pre_rank=rank
    profile.pre_gl=grade_level.split("/")[0]
    profile.pre_salary=salary_grade_level 
    profile.date_of_last_promotion=last_promotion 
    profile.staff_no=staff_no 
    profile.occupant=occupant 
    profile.nok_name_1=nok_name_1 
    profile.nok_address_1=nok_address_1 
    profile.nok_relationship_1=nok_relationship_1
    profile.nok_name_2=nok_name_2
    profile.nok_address_2=nok_address_2
    profile.nok_relationship_2=nok_relationship_2
    profile.account_num=""
    profile.save()

def do_some_stuffs():
    print "++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++"
    print Profile.objects.all()
    print "++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++"


