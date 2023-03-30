from django.http import HttpResponse, JsonResponse
import json
from bson.json_util import dumps
import pymongo

from . import models

def stations(request):
    if(request.method == "GET"):
        return get(request)
    elif(request.method == "POST"):
        return post(request)
    elif(request.method == "PUT"):
        return put(request)
    elif(request.method == "DELETE"):
        return delete(request)
    
def get(request):
    body = request.body.decode('utf-8')
    if(len(body) > 0):
        print("long")
        json_data = json.loads(body)
        try:
            cursor = stations.search(json_data['search_terms'])
        except:
            cursor = stations.find(json_data['limit'])
    else:
        print("short")
        cursor = stations.find(10)
    cursor_list = list(cursor)
    json_data = dumps(cursor_list)
    return JsonResponse(json_data, safe=False)

def post(request):
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    if(json_data['bulk'] == "false"):
        response = stations.create(json_data)
    elif(json_data['bulk'] == "true"):
        response = stations.bulk_create(json_data)
    return HttpResponse()

def put(request):
    return HttpResponse()

def delete(request):
    body = request.body.decode('utf-8')
    try:
        json_data = json.loads(body)
    except:
        return HttpResponse("false")
    if(json_data['bulk'] == "false"):
        response = stations.delete(json_data)
    elif(json_data['bulk'] == "true"):
        response = stations.bulk_delete(json_data)
    return HttpResponse(response)