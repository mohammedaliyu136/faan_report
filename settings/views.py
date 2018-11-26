# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from report.models import TableTitle, ColTitle, TableData

# Create your views here.
def index(request): 
    return render(request, "sdfg.html", {})

def create_table(request):
    error = ""
    success = ""
    if request.method == 'POST':
        table_title = request.POST.get('table_title')
        num_of_cols = request.POST.get('num_of_cols')
        
        table_object = TableTitle.objects.filter(title=table_title)
        if(len(table_object)>=1):
            error = "Table already exist!!!!"
        else:
            error = ""
            TableTitle(title=table_title).save()
            table_object = TableTitle.objects.get(title=table_title)
            for col in range(1,int(num_of_cols)+1):
                col = request.POST.get('col_'+str(col))
                ColTitle(title = col, table_id = str(table_object.pk)).save()
                success = "Added successfully"
    print TableTitle.objects.all()
    print ColTitle.objects.all()
        
    return render(request, "create_table.html", {"error":error, "success":success})

def tab(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        col_id   = request.POST.get('col_id')
        method   = request.POST.get('method')
        col_id = col_id.split(" ")
        col_id.pop()
        if(method=="delete"):
            tiltle = TableTitle.objects.get(title=table_id)
            for col in col_id:
                TableData.objects.get(id = col).delete() 
        else:
            pass

    tiltle = TableTitle.objects.get(title="staff list")
    col = ColTitle.objects.filter(table_id = str(tiltle.pk))
    data = TableData.objects.filter(table_id = str(tiltle.pk))
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
    

    return render(request, "drawTable.html", {"tiltle":tiltle, "cols":col, "data":data, "rows":row})

def input_data(request):
    #name	age	address	status
    tiltle = TableTitle.objects.get(title="staff list")
    cols = ColTitle.objects.filter(table_id = str(tiltle.pk)) 
    #tableId = TableTitle.objects.get(table_id = str(tiltle.pk))
    if request.method == 'POST':
        
        for col in cols:
            #table_id
            d = request.POST.get(col.title)
            table_id = request.POST.get('table_id')
            TableData(col_id=col.id, data=d, table_id=table_id).save()
    return render(request, "insertData.html", {"tiltle":tiltle, "cols":cols})
    