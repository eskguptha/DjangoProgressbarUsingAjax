from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from datetime import datetime, date
from django.conf import settings
import json
import sqlite3
from django.db import connection
import datetime



def load_home(request):
    variables = {}

    return render_to_response("loadapp/home.html", RequestContext(request, variables))

def load_status_all(request):
    start  = (datetime.datetime.now() - datetime.timedelta(days=999)).strftime('%Y-%m-%d')
    end = (datetime.datetime.now() + datetime.timedelta(days=999)).strftime('%Y-%m-%d')
    dates = start+' - '+end
    if request.POST:
        dates = request.POST.get('dates', None)
        if dates:
            start, end = dates.split(' - ')
    #print dates, start, end
    cursor=connection.cursor()
    query = "SELECT * FROM paramfile_status WHERE created_date between '%s' and '%s'  ORDER BY created_date DESC "%(start, end)
    cursor.execute(query)
    result = cursor.fetchall()
    variables = {"status_table" : result, 'dates':dates, "start":start,"end":end}
    return render_to_response("loadapp/task_list.html", RequestContext(request, variables))

def load_status_view(request, sid):
    cursor=connection.cursor()
    if int(sid)>0:
        query1 = "SELECT * FROM paramfile_status WHERE paramfile_id = %s "%sid
    else:
        query1 = "SELECT TOP 1 * FROM paramfile_status ORDER BY paramfile_id DESC "
    cursor.execute(query1)
    result1 = cursor.fetchall()
    if result1:
        sid = int(result1[0][0])
    query2 = "SELECT * FROM load_status WHERE paramfile_id = '%s' "%sid
    cursor.execute(query2)
    result2 = cursor.fetchall()
    variables = {"paramfile_status" : result1, 'load_status':result2}
    return render_to_response("loadapp/task_detail_view.html", RequestContext(request, variables))


def load_status_table(request, paramfile_id, load_status):
    if load_status=='Not_yet_loaded':
        load_status = 'Not yet loaded'
    cursor=connection.cursor()
    query1 = "SELECT * FROM paramfile_status WHERE paramfile_id = '%s'  "%int(paramfile_id)
    cursor.execute(query1)
    result1 = cursor.fetchall()
    query2 = "SELECT * FROM load_status WHERE paramfile_id = '%s' and status = '%s' "%(paramfile_id, load_status)
    cursor.execute(query2)
    result2 = cursor.fetchall()
    variables = {
                'paramfile_status_rows' : result1,
                'load_status_rows':result2,
                'load_status':load_status,
                'paramfile_id':paramfile_id
                }
    return render_to_response("loadapp/load_status_table.html", RequestContext(request, variables))



def getStatus():
    load_status_result = ()
    paramfile_path = ''
    paramfile_id = 0
    doc_count = {}
    cursor=connection.cursor()
    query = "SELECT  paramfile_id, paramfile_path,load_status FROM paramfile_status WHERE load_status='Processing' ORDER BY created_date DESC"
    cursor.execute(query)
    load_status_result = cursor.fetchone()
    if load_status_result:
        paramfile_id = load_status_result[0]
        paramfile_path = load_status_result[1]
        query = "SELECT file_path, source_Nrrows, processed_Nrrows FROM load_status WHERE paramfile_id='%s' and status ='Processing'  "%paramfile_id
        cursor.execute(query)
        load_status_result=cursor.fetchall()
        for row in load_status_result:
            tab_separated_file_path = row[0]
            source_Nrrows = row[1]
            processed_Nrrows = row[2]
            doc_count[tab_separated_file_path] = (int(processed_Nrrows),int(source_Nrrows))

    return doc_count, paramfile_path, paramfile_id

def load_status(request):
    doc_count,paramfile_path, paramfile_id = getStatus()
    if doc_count:
        status = 1
    else:
        status = 0

    variables = {   "doc_count":doc_count,
                    "no_of_workers":len(doc_count.keys()),
                    "paramfile_id":paramfile_id,
                    "status":status,

                }
    return render_to_response("loadapp/status.html", RequestContext(request, variables))


def progress_bar(request):
    input_data = {}
    output_data = {}
    if request.is_ajax():
        print "Ajax call started"
        input_data, paramfile_path, paramfile_id = getStatus()
        if input_data:
            for each_file, value in input_data.items():
                processed_Nrrows = int(value[0])
                source_Nrrows = int(value[1])
                if processed_Nrrows > 0:
                    output_data[each_file]=round((processed_Nrrows*100.0)/source_Nrrows,0)
                else:
                    output_data[each_file] = 0

    if output_data == {}:
        output_data['status'] = 0
    return HttpResponse(json.dumps(output_data), content_type="application/json")
