#Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps
import pymongo
from . import models
from bson.objectid import ObjectId
#Stations View
#Splits the request into the appropriate methods
@csrf_exempt
def stations(request):
    if(request.method == "GET"):
        return get(request)
    elif(request.method == "POST"):
        return post(request)
    elif(request.method == "PUT"):
        return put(request)
    elif(request.method == "DELETE"):
        return delete(request)
    elif(request.method == "PATCH"):
        return patch(request)
    elif(request.method == "OPTIONS"):
        return options(request)
#Get
#Gets a station or stations
#Parameters: limit (int)
#[localhost:8000/stations?limit=(limit)]
'''
localhost:8000/stations/?id=dlb_atm41_5282
'''
def get(request):
    query = request.GET
    if 'limit' in query or 'id' in query:
        cursor = models.find(query.get('id', ""), int(query.get('limit', 10)))
    else:
        cursor = models.find(10)
    return JsonResponse(dumps(list(cursor)), safe=False)

#Post
#Creates a new station or stations
#Parameters: new (record/array), bulk (boolean)
#[localhost:8000/stations] {"new": {(key): (value)}}
'''
{
    "bulk": "false",
    "new": [
            {
                "_id": "dlb-atm-41-5281",
                "Device Name": "DLB ATM41 Speers Point Pool",
                "State": "NSW",
                "Latitude": "-32.96305",
                "Longitude": "151.61993",
                "Last Response": ""
            }
            ]
}
'''
def post(request):
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    response = models.create(json_data)
    models.station_trigger()
    return HttpResponse(response)

#Put
#Updates a station or stations
#Parameters: search_terms, new (record/array), bulk (boolean)
#[localhost:8000/stations] {"bulk":(true/false), "search_terms": {(key): (value)}, "new": {(key): (value)}}
'''
{
  "bulk": "false",
  "search_field":"Device Name", "search_term":"DLB ATM41 Charlestown Skate Park", "update_field":"Device Name", "update_value":"DLB ATM41 Possibly Charlestown Skate Park", "limit":100
}
'''
def put(request):
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    #Get bulk parameter
    bulk = json_data.get('bulk', "false")
    #Check if this is a bulk update
    if bulk == "false":
        response = models.update({json_data['search_field']:json_data['search_term']}, {'$set':{json_data['update_field']:json_data['update_value']}})
    elif bulk == "true":
        if 'limit' in json_data:
            response = models.bulk_update({json_data['search_field']:json_data['search_term']}, {'$set':{json_data['update_field']:json_data['update_value']}}, int(json_data['limit']))
        else:
            response = models.bulk_update({json_data['search_field']:json_data['search_term']}, {'$set':{json_data['update_field']:json_data['update_value']}})
    return HttpResponse(response)

#Patch
#Updates a station or stations
#Parameters: search_terms, new (record/array), bulk (boolean)
#[localhost:8000/stations] {"bulk":(true/false), "search_terms": {(key): (value)}, "new": {(key): (value)}}
# Example: localhost:8000/stations
#    {"bulk":"false", "search_terms": {"$oid": "64251a6bc0bde0d5eea40532"}, "new": {"Longitude": "-83.3792"}}

'''
def patch(request):
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
'''
def patch(request):
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    #Get bulk parameter
    bulk = json_data.get('bulk', "false")
    #Check if this is a bulk update
    if bulk == "false":
        response = models.update({json_data['search_field']:json_data['search_term']}, {'$set':{json_data['update_field']:json_data['update_value']}})
    elif bulk == "true":
        if 'limit' in json_data:
            response = models.bulk_update({json_data['search_field']:json_data['search_term']}, {'$set':{json_data['update_field']:json_data['update_value']}}, int(json_data['limit']))
        else:
            response = models.bulk_update({json_data['search_field']:json_data['search_term']}, {'$set':{json_data['update_field']:json_data['update_value']}})
    return HttpResponse(response)
#Delete
#Deletes a station or stations
#Parameters: search_terms, bulk (boolean)
#[localhost:8000/stations/?bulk=true] {"search_terms": {(key): (value)}}
'''
{
  "bulk": "false",
  "search_terms":
  {
      "Device Name": "Dummy Station"
  }
}
'''
def delete(request):
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    if 'oid' in json_data:
        response = models.delete({'_id': ObjectId(json_data['oid'])})
    else:
        bulk = json_data.get('bulk', "false")
        if bulk == "false":
            response = models.delete(json_data['search_terms'])
        elif bulk == "true":
            response = models.bulk_delete(json_data['search_terms'])
    return HttpResponse(response.deleted_count)

#Options
#Returns the options for the stations view
def options(request):
    return HttpResponse("GET, POST, PUT, DELETE, PATCH, OPTIONS")