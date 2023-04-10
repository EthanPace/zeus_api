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
#localhost:8000/analytics?field=precipitation&aggregation=max
def get(request):
    parameters = request.GET
    response = models.get_aggregation(parameters['field'], parameters['aggregation'])
    return JsonResponse(dumps(list(response)), safe=False)