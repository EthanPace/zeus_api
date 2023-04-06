#Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps
from . import models
#Weather View
#Splits the request into the appropriate methods
@csrf_exempt
def weather(request):
    if(request.method == "GET"):
        return get(request)
    elif(request.method == "POST"):
        return post(request)
    elif(request.method == "PUT"):
        return put(request)
    elif(request.method == "DELETE"):
        return delete(request)
#Get
#Returns ten records (default), or a specified number of records, or a specific record based on search terms
#Parameters: none
def get(request):
    query = request.GET
    if 'limit' in query or 'oid' in query and not 'time' in query and not 'device_id' in query:
        print("find")
        print(query)
        cursor = models.find(query.get('oid', ""), int(query.get('limit', 10)))
    elif 'time' in query or 'device_id' in query:
        print("search")
        print(query)
        cursor = models.search(query)
    else:
        print("default")
        print(query)
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
def put(request):
    body = request.body.decode('utf-8')
    try:
        json_data = json.loads(body)
        if 'bulk' in json_data:
            if json_data['bulk'] == "false":
                response = models.update(json_data['search_terms'], json_data['new'])
            elif json_data['bulk'] == "true":   
                response = models.bulk_update(json_data['search_terms'], json_data['new'])
        else:
            response = models.update(json_data['search_terms'], json_data['new'])
    except:
        return JsonResponse({'result':'false'})
    return HttpResponse(response)
#Delete
#Deletes a record or records
#Parameters: search_terms, bulk (boolean)
def delete(request):
    body = request.body.decode('utf-8')
    try:
        json_data = json.loads(body)
        if 'bulk' in json_data:
            if json_data['bulk'] == "false":
                response = models.delete(json_data['search_terms'])
            elif json_data['bulk'] == "true":   
                response = models.bulk_delete(json_data['search_terms'])
        else:
            response = models.delete(json_data['search_terms'])
    except:
        return JsonResponse({'result':'false'})
    return HttpResponse(response)