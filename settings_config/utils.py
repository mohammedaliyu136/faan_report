import csv
from time import strptime


from employee.models import Profile, AcademicProfessionalQualification
from ems_september import settings
from ems_september.settings import PROJECT_ROOT


def save_emp():
    d = []
    with open(PROJECT_ROOT+"\\raw_data\\staff_list.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print ""+','.join(row)
                d.append(row)
            else:
                print ""+','.join(row)
                d.append(row)
            line_count+=1
        print "processed "+str(line_count)

    for i in d:
        names = i[0].split(" ")#[0]+i[0].split(" ")[1]
        if len(names)<2:
            print "@@@@@@@@@@@@@@@@@@@@"
        else:
            pass
            #Profile(surname = i[0].split(" ")[0],othername = i[0].split(" ")[1],title = i[1],gender = i[2],date_of_birth = i[3],staff_no = i[4],designation = i[6],pre_gl = i[7],date_of_first_Appt = i[8],date_of_conf = i[9],date_of_last_promotion = [10],lga = i[11],state = i[12], occupant=False).save()
            #print "Added: "+i[0].split(" ")[0]+" "+i[0].split(" ")[1]+" successfully..."

def save_emp_import():
    d = []
    with open(PROJECT_ROOT+"\\raw_data\\nov\\audit.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print ""+','.join(row)
                d.append(row)
            else:
                if len(row)>0:
                    #print ""+','.join(row)
                    d.append(row)
            line_count+=1
        print "processed "+str(line_count)

    d2 = []
    with open(PROJECT_ROOT+"\\raw_data\\nov\\staff_l.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print ""+','.join(row)
                d2.append(row)
            else:
                if len(row)>0:
                    #print ""+','.join(row)
                    d2.append(row)
            line_count+=1
        print "processed "+str(line_count)

    for a in d:
        for sec in d2:
            n = False
            if len(sec)>2:
                if len(a)>2:
                    #print a[2].split(" ")[0]#,a[2].split(" ")[1]
                    if a[2] in sec[1].upper() or (a[2].split(" ")[0] in sec[1].upper() and sec[8]==a[4]):# or (a[2].split(" ")[1] in sec[1].upper() and  sec[8]==a[4]):
                        #print a[2], sec[1].upper()
                        #c+=1
                        for s in sec:
                            a.append(s)

    for a in d:
        if len(a)==1:
            department = a[0]
        else:
            #print a
            nt_quartered = "NOT QUARTERED "
            quartered = "QUARTERED"
            quarters = ""
            if(a[6]==quartered):
                quarters = True
            else:
                quarters = False
            names = a[2].split(" ")
            if len(names)<2:
                print "@@@@@@@@@@@@@@@@@@@@"
            else:
                if(len(a)==22):
                    if(len(names)>2):
                        surname = names[0]
                        firstname = names[1]
                        othername = names[2]#,
                        pass
                    else:
                        surname = names[0]
                        firstname = names[1]
                        othername = ""
                    title = a[10]#,gender = a[13]#,date_of_birth = a[13],staff_no = a[14],designation = a[16],pre_gl = a[17],date_of_first_Appt = a[18],date_of_conf = a[19],date_of_last_promotion = a[20],lga = a[21],state = a[22], occupant=quarters, department=department, status=a[7]
                    staff_no = a[13]
                    date_of_birth = a[12]
                    gl = a[16]
                    pre_gl=""
                    if(len(a[16].split("-"))>1):
                        gl = a[16].split("-")
                        pre_gl = strptime(gl[1],'%b').tm_mon
                        gl = str(strptime(gl[1],'%b').tm_mon)+"/"+str(gl[0])
                    designation = a[15]
                    date_of_first_Appt = a[17]
                    date_of_conf = a[18]
                    date_of_last_promotion = a[19]
                    lga = a[20]
                    state = a[21]
                    occupant=quarters
                    department=department
                    status=a[7]
                    gender = a[11]
                    account_num = a[13]
                    #print surname, firstname, othername, title,gender, department, status, staff_no, gl, date_of_birth, designation, date_of_first_Appt, date_of_conf, date_of_last_promotion, lga, state
                    Profile(surname = surname, othername=firstname,maidenname = othername,title = title,gender = gender,date_of_birth = date_of_birth,staff_no = staff_no,designation = designation,gl = gl,date_of_first_Appt = date_of_first_Appt,date_of_conf = date_of_conf,date_of_last_promotion = date_of_last_promotion,lga = lga,state = state, occupant=occupant, department=department, status=status, account_num=account_num, pre_gl=pre_gl).save()
                    #print surname, firstname, othername, a[10], a[11],a[12],a[13],a[14],a[16],a[17],a[18],a[19],a[20],a[21],quarters,department, a[7]#,a[22]
                    #print surname, firstname, othername, a[10], a[11],a[12],a[13],a[16],a[17],a[18],a[19],a[20],a[21],quarters,department, a[7]#,a[22]#,a[14],a[16],a[17],a[18],a[19],a[20],a[21],quarters,department, a[7]#,a[22]
            #Profile(surname = i[0].split(" ")[0],othername = i[0].split(" ")[1],title = i[1],gender = i[2],date_of_birth = i[3],staff_no = i[4],designation = i[6],pre_gl = i[7],date_of_first_Appt = i[8],date_of_conf = i[9],date_of_last_promotion = [10],lga = i[11],state = i[12], occupant=False).save()
                #['S/N', 'STAFF NO ACCT. (PAYROLL)', 'FULL NAME SURNAME FIRST', 'DESIGNATION', 'GL/STEP', 'DEPARTMENT', 'OCCUPANT OF STAFF QUARTERS', 'MARITAL STATUS', 'REMARKS']

                    #print a[11],a[12],a[13],a[14],a[16],a[17],a[18],a[19],a[20],a[21],quarters,department, a[7]#,a[22]
                    print "Added: "+a[2]+" successfully imported..."


def save_emp_import_v2():
    d2 = []
    with open(PROJECT_ROOT+"\\raw_data\\nov\\staff_l.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print ""+','.join(row)
                d2.append(row)
            else:
                if len(row)>0:
                    #print ""+','.join(row)
                    d2.append(row)
            line_count+=1
        print "processed "+str(line_count)

def save_emp_import_v3():
    d2 = []
    counter=0
    #with open(PROJECT_ROOT+"\\raw_data\\nov\\staff_l.csv") as csv_file:
    with open(PROJECT_ROOT+"\\raw_data\\nov\\data.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print ""+','.join(row)
                d2.append(row)
            else:
                if len(row)>0:
                    #print ""+','.join(row)
                    d2.append(row)
            line_count+=1
        print "finished staff list data... "

    audit_d = []
    with open(PROJECT_ROOT+"\\raw_data\\nov\\audit.csv") as csv_file:
        counter = 0
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                audit_d.append(row)
            else:
                if len(row)>0:
                    audit_d.append(row)
            line_count+=1
        print "finished audit list data..."

    q = 0
    for d in d2:
        if len(d)==1:
            department_staff_list = d[0]
        else:
            if len(d)>1:
                surname = d[1].split(" ")[0]
                lastname = d[1].split(" ")[1]
                designation = d[3]
                gl_step = d[8]
                for a_d in audit_d:
                    if len(a_d)==1:
                        department_audit_list = a_d[0]
                    else:
                        if len(a_d)>1:
                            surname_audit = a_d[2].split(" ")[0]
                            lastname_audit = a_d[2].split(" ")[1]
                            designation_audit = a_d[3]
                            gl_step_audit = a_d[4]
                            #print surname.upper(), surname_audit, lastname.upper(), lastname_audit, department_staff_list, department_audit_list

                            if department_staff_list == department_audit_list:
                                if (surname.upper() == surname_audit and lastname.upper() == lastname_audit) or (surname.upper() == surname_audit and gl_step==gl_step_audit):
                                    q+=1
                                    staff_no = a_d[1]
                                    occupant = a_d[6]
                                    status = a_d[7]
                                    d.append(staff_no)
                                    d.append(occupant)
                                    d.append(status)
                counter+=1



    counter = 0
    for d in d2:
        if len(d)==1:
            print "++++++++++++++department++++++++++++++++++"
            department = d[0]
            print "++++++++++++++++++++++++++++++++++++++++++"
        else:
            counter+=1
            if len(d)>1:
                names = d[1].split(" ")
                if(len(names)>2):
                    surname = names[0]
                    firstname = names[1]
                    othername = names[2]
                else:
                    surname = names[0]
                    firstname = names[1]
                    othername = ""
            #print ",".join(d)
            if len(d)==14:
                gl = d[8].split("/")
                pre_gl = gl[0]
                gl = d[8]
                Profile(surname = surname, othername=firstname,maidenname = othername,title = d[2],gender = d[3],date_of_birth = d[4],staff_no = d[5],designation = d[7],gl = gl,date_of_first_Appt = d[9],date_of_conf = d[10],date_of_last_promotion = d[11],lga = d[12],state = d[13],department=department, pre_gl=pre_gl, occupant=False).save()
                profs = Profile.objects.filter(surname = surname, othername=firstname, department=department)
                prof_id = profs[0].id
                AcademicProfessionalQualification(profile_id=prof_id, name=d[6]).save()
                print "added: "+ " ".join(names) + "successfully..."
            elif len(d)==17 or len(d)>17:
                quartered = ""
                if(d[15]=="QUARTERED"):
                    quartered = True
                else:
                    quartered = False
                status = d[16]
                gl = d[8].split("-")
                #if len(gl)>1:
                #    pre_gl = strptime(gl[1],'%b').tm_mon
                #    gl = str(strptime(gl[1],'%b').tm_mon)+"/"+str(gl[0])
                pre_gl = d[8].split("/")[0]
                gl = d[8]
                Profile(surname = surname, othername=firstname,maidenname = othername,title = d[2],gender = d[3],date_of_birth = d[4],staff_no = d[5],designation = d[7],gl = gl,date_of_first_Appt = d[9],date_of_conf = d[10],date_of_last_promotion = d[11], lga = d[12], state = d[13], occupant=quartered, department=department, status=status, account_num=d[14], pre_gl=pre_gl).save()
                profs = Profile.objects.filter(surname = surname, othername=firstname, department=department)
                prof_id = profs[0].id
                AcademicProfessionalQualification(profile_id=prof_id, name=d[6]).save()
                print "added: "+ " ".join(names) + "successfully..."


def fix_data_import():
    profiles = Profile.objects.all()
    for profile in profiles:
        #profile.pre_gl = profile.pre_gl.split("/")[0]
        #profile.save()
        pre_gl = str(profile.gl).split("/")
        profile.pre_gl = pre_gl[0]
        profile.save()
        print profile.surname + "  done...."
