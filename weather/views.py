#Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from . import models
#Weather View
#Splits the request into the appropriate methods
@csrf_exempt
def weather(request):
    if(request.method == "GET"):
        return get(request)
    elif(request.method == "POST"):
        return post(request)
    elif(request.method == "PATCH"):
        return patch(request)
    elif(request.method == "DELETE"):
        return delete(request)
#Get
#Returns ten records (default), or a specified number of records, or a specific record based on search terms
#Parameters: none
def get(request):
    query = request.GET
    if 'time' in query or 'device_id' in query:
        cursor = models.search(query)
    elif 'limit' in query or 'oid' in query:
        cursor = models.find(query.get('oid', ""), int(query.get('limit', 10)))
    else:
        cursor = models.find("",10)
    cursor_list = list(cursor)
    json_data = dumps(cursor_list)
    return JsonResponse(json_data, safe=False)
#Post
#Creates a new record or records
#Parameters: new (record/array), bulk (boolean)
def post(request):
    body = request.body.decode('utf-8')
    bulk = request.POST.get('bulk', "false")
    json_data = json.loads(body)
    if bulk == "false":
        response = models.create(json_data)
    elif bulk == "true":
        response = models.bulk_create(json_data)
    return HttpResponse(response)
#Put
#Updates a record or records
#Parameters: search_terms, new (record/array), bulk (boolean)
def patch(request):
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    bulk = json_data.get('bulk', "false")
    limit = int(json_data.get('limit', 10))
    oid = json_data.get('oid', "false")
    print ("================ PATCH ==================")
    print ("== body ==")
    print (body)
    print ("== request ==")
    print (request)
    print ("== request.PATCH ==")
    print (request)
    print ("== bulk ==")
    print (bulk)
    print (json_data)
    if bulk == "false":
        print ("===== bulk false =====")
        print ("== search_terms ==")
        print (json_data['search_terms'])
        print ("== new ==")
        print (json_data['new'])
        response = models.update(json_data['search_terms'], json_data['new'])
    elif bulk == "true":
        print ("===== bulk true =====")
        print ("== search_terms ==")
        print (json_data['search_terms'])
        print ("== new ==")
        print (json_data['new'])
        response = models.bulk_update(json_data['search_terms'], json_data['new'])
    return HttpResponse(response)
#Delete
#Deletes a record or records
#Parameters: search_terms, bulk (boolean)
def delete(request):
    body = request.body.decode('utf-8')
    bulk = request.POST.get('bulk', "false")
    json_data = json.loads(body)
    if bulk == "false":
        response = models.delete(json_data)
    elif bulk == "true":
        response = models.bulk_delete(json_data)
    return HttpResponse(response)
