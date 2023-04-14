#Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
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
#Get
#Returns ten records (default), or a specified number of records, or a specific record based on search terms
#Parameters: none
@require_http_methods(["GET"])
def get(request):
    query = request.GET
    if 'time' in query or 'device_id' in query:
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
@require_http_methods(["POST"])
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
@require_http_methods(["PUT"])
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

@require_http_methods(["DELETE"])
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

'''
#Delete
#Deletes a record or records
@require_http_methods(["DELETE"])
def delete(request):
    print("Delete chosen")
    query = request.GET
    if 'oid' in query:
        result = models.delete({'_id': ObjectId(query.get('oid'))})
        print(ObjectId(query.get('oid')))
        response = {'deleted_count': result.deleted_count}
    else:
        response = {'message': 'Please provide an oid to delete.'}
    return JsonResponse(response, safe=False)
'''