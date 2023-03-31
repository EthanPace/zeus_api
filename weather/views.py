#Imports
from django.http import HttpResponse, JsonResponse
import json
from bson.json_util import dumps
from . import models
#Weather View
#Splits the request into the appropriate methods
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
#Returns a list of records or one record based on search terms
#Parameters: search_terms (dict/array), limit (int)
def get(request):
    body = request.body.decode('utf-8')
    try:
        json_data = json.loads(body)
        if 'limit' in json_data:
            cursor = models.find(json_data['limit'])
            cursor_list = list(cursor)
            json_data = dumps(cursor_list)
            return JsonResponse(json_data, safe=False)
        elif 'search_terms' in json_data:
            cursor = models.search(json_data['search_terms'])
    except:
        cursor = models.find(10)
        cursor_list = list(cursor)
        json_data = dumps(cursor_list)
        return JsonResponse(json_data, safe=False)
#Post
#Creates a new record or records
#Parameters: new (record/array), bulk (boolean)
def post(request):
    body = request.body.decode('utf-8')
    try:
        json_data = json.loads(body)
        if 'bulk' in json_data:
            if json_data['bulk'] == "false":
                response = models.create(json_data['new'])
            elif json_data['bulk'] == "true":   
                response = models.bulk_create(json_data['new'])
        else:
            response = models.create(json_data['new'])
    except:
        return JsonResponse({'result':'false'})
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