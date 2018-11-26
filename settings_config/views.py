# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from report.models import TableTitle, ColTitle


# Create your views here.
from settings_config.utils import *

def fix_gl(request):
    profiles = Profile.objects.filter(department="SECURITY")
    if request.POST:
        for profile in profiles:
            gl = request.POST.get(str(profile.id)+"_gl")
            pre_gl = request.POST.get(str(profile.id)+"_pregl")
            #print profile.surname+" "+profile.othername+" gl:"+str(gl)+"  pre gl:"+str(pre_gl)
            profile.gl = gl
            profile.pre_gl = pre_gl
            profile.save()
            print str(profile.id)+" done---"

    return render(request, "set_config/fix_gl.html", {"profiles":profiles})

def index(request):
    tables = TableTitle.objects.all()
    #save_emp()
    #save_emp_import()
    #save_emp_import_v3()
    #fix_data_import()
    if request.method == 'POST':
        title = request.POST.get('title')
        TableTitle(title=title).save()
        table_object = TableTitle.objects.get(title=title)
        ids = request.POST.get('ids')
        ids = ids.split(",")
        for i in ids:
            col = request.POST.get(i)
            col_type = request.POST.get(i + "_type")
            col_link = request.POST.get(i + "_link")
            ColTitle(title=col, field_type=col_type,emp_field=col_link, table_id=str(table_object.pk)).save()
    return render(request, "set_config/index.html", {"tables": tables})


def create_table(request):
    error = ""
    success = ""
    if request.method == 'POST':
        table_title = request.POST.get('table_title')
        num_of_cols = request.POST.get('num_of_cols')

        table_object = TableTitle.objects.filter(title=table_title)
        if len(table_object) >= 1:
            error = "Table already exist!!!!"
        else:
            error = ""
            TableTitle(title=table_title).save()
            table_object = TableTitle.objects.get(title=table_title)
            print '---------------------------------------------'
            for col in range(1, int(num_of_cols) + 1):
                col = request.POST.get('col_' + str(col))
                col_type = request.POST.get('col_type_' + str(col))
                print col_type
                print 'col_type_' + str(col)
                ColTitle(title=col, field_type=col_type, table_id=str(table_object.pk)).save()
                success = "Added successfully"
    table_title = TableTitle.objects.all()
    print ColTitle.objects.all()

    return render(request, "create_table.html", {"error": error, "success": success, "table_title": table_title})
