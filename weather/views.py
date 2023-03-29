from django.http import HttpResponse, JsonResponse
from bson.json_utils import dumps
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
    json_data = dumps(cursor_list)
    return JsonResponse(json_data)

def post(request):
    return HttpResponse()
def put(request):
    return HttpResponse()
def delete(request):
    return HttpResponse()