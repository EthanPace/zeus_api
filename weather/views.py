#Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps
from . import models
from bson.objectid import ObjectId

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
    elif(request.method == "OPTIONS"):
        return options(request)
#Get
#Returns ten records (default), or a specified number of records, or a specific record based on search terms
#Parameters: none
def get(request):
    query = request.GET
    if 'page' in query:
        cursor = models.page(int(query['page_size']), int(query['page'])) #[localhost:8000/weather?page_size=10&page=1]
    elif 'time' in query or 'device_id' in query:
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
'''
{
  "bulk": "true",
  "new": [
    {
      "Time": "2022-01-01T00:00:00+00:00",
      "Device ID": "dlb-atm41-0001",
      "Device Name": "DLB ATM41 Test Device 1",
      "Latitude": 45.123456,
      "Longitude": -122.123456,
      "Temperature (\u00b0C)": 20.5,
      "Atmospheric Pressure (kPa)": 101.325,
      "Lightning Average Distance (km)": 0.0,
      "Lightning Strike Count": 0.0,
      "Maximum Wind Speed (m/s)": 2.0,
      "Precipitation mm/h": 0.0,
      "Solar Radiation (W/m2)": 0.0,
      "Vapor Pressure (kPa)": 2.0,
      "Humidity (%)": 60.0,
      "Wind Direction (\u00b0)": 180.0
    },
    {
      "Time": "2022-01-02T00:00:00+00:00",
      "Device ID": "dlb-atm41-0002",
      "Device Name": "DLB ATM41 Test Device 2",
      "Latitude": 45.654321,
      "Longitude": -122.654321,
      "Temperature (\u00b0C)": 18.0,
      "Atmospheric Pressure (kPa)": 101.0,
      "Lightning Average Distance (km)": 0.0,
      "Lightning Strike Count": 0.0,
      "Maximum Wind Speed (m/s)": 1.5,
      "Precipitation mm/h": 0.0,
      "Solar Radiation (W/m2)": 0.0,
      "Vapor Pressure (kPa)": 1.8,
      "Humidity (%)": 70.0,
      "Wind Direction (\u00b0)": 270.0
    }
  ]
}
'''
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

#Delete
#Deletes a record or records
#Parameters: search_terms, bulk (boolean)
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
#Returns the allowed methods
def options(request):
    return HttpResponse("GET, POST, PUT, DELETE, OPTIONS")