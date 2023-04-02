#Imports
from django.http import HttpResponse, JsonResponse
import json
from bson.json_util import dumps
import pymongo
from . import models
#Analytics View
#Splits the request into the appropriate methods
def analytics(request):
    if(request.method == "GET"):
        return get(request)
#Get
#Returns the aggregated data on the chosen column
#Parameters: field, aggregation
def get(request):
    body = request.body.decode('utf-8')
    try:
        json_data = json.loads(body)
        response = models.get_aggregation(json_data['field'], json_data['aggregation'])
    except:
        return HttpResponse("body must be json with field and aggregation")
    return JsonResponse(dumps(response))