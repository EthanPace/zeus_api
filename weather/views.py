from django.http import HttpResponse, JsonResponse
import json
import pymongo

from . import models

def weather(request):
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
        json_data = json.loads(body)
        try:
            cursor = models.search(json_data['search_terms'])
        except:
            cursor = models.find(json_data['limit'])
    else:
        cursor = models.find(10)
    cursor_list = list(cursor)
    json_data = cursor_list
    return JsonResponse(json_data)

def post(request):
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    if(json_data['bulk'] == "false"):
        response = models.create(json_data)
    elif(json_data['bulk'] == "true"):
        response = models.bulk_create(json_data)
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
        response = models.delete(json_data)
    elif(json_data['bulk'] == "true"):
        response = models.bulk_delete(json_data)
    return HttpResponse(response)