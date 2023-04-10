#Imports
from django.http import HttpResponse, JsonResponse
import json
from bson.json_util import dumps
import pymongo
from . import models
#Stations View
#Splits the request into the appropriate methods
def stations(request):
    if(request.method == "GET"):
        return get(request)
    elif(request.method == "POST"):
        return post(request)
    elif(request.method == "PUT"):
        return put(request)
    elif(request.method == "DELETE"):
        return delete(request)
#Get
#Gets a station or stations
#Parameters: limit (int)
def get(request):
    g = request.GET
    if 'limit' in g:
        cursor = models.find(g['limit'])
    else:
        cursor = models.find(10)
    return JsonResponse(dumps(list(cursor)), safe=False)

#Post
#Creates a new station or stations
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
        return HttpResponse("false")
    models.station_trigger()
    return HttpResponse(response)
#Put
#Updates a station or stations
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
        return HttpResponse("false")
    return HttpResponse(response)
#Delete
#Deletes a station or stations
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
        return HttpResponse("false")
    return HttpResponse(response)