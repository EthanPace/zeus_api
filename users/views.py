#Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps
from . import models
from hashlib import sha256
from django.views.decorators.http import require_http_methods
from bson.objectid import ObjectId
#User View
#Splits the request into the appropriate methods
@csrf_exempt
def users(request):
    if(request.method == "GET"):
        return get(request)
    elif(request.method == "POST"): 
        return post(request)
    elif(request.method == "PUT"):
        return put(request)
    elif(request.method == "DELETE"):
        return delete(request)

''' 
#Get
#Returns ten records
#Parameters: none
#[localhost:8000/users/]
def get(request):
    #Use the get "model" to get the records
    cursor = models.get(10)
    #Convert the cursor to a list, then to JSON
    response = dumps(list(cursor))
    #Return the response
    return JsonResponse(response, safe=False)
'''

#Get
#Returns ten records (default), or a specified number of records, or a specific record based on search terms
#Parameters: none
def get(request):
    query = request.GET
    #if 'time' in query or 'device_id' in query:
    #    cursor = models.search(query)
    if 'limit' in query or 'oid' in query:
        cursor = models.find(query.get('oid', ""), int(query.get('limit', 10)))
    else:
        cursor = models.find("",10)
    cursor_list = list(cursor)
    json_data = dumps(cursor_list)
    return JsonResponse(json_data, safe=False)

#Post
#Creates a new record or records
#Parameters: new (record/array), bulk (boolean)
#[localhost:8000/users/] {"bulk":"true/false", "users": [{"username":"(username)", "password":"(password)"}, {"username":"(username)", "password":"(password)"}]}
def post(request):
    #Get the request body in sring format
    body = request.body.decode('utf-8')
    #Parse the body as JSON
    json_data = json.loads(body)
    #Check if the request is a bulk operation
    if json_data['bulk'] == "true":
        #Get the request body in sring format
        body = request.body.decode('utf-8')
        #Parse the body as JSON
        json_data = json.loads(body)
        #Hash the passwords
        hashes = []
        for user in json_data['users']:
            hashes.append(hash(user['Password']))
        #Use the create "model" to create the records
        response = models.bulk_create(json_data['users'], hashes)
        id_ = response.inserted_ids
    else:
        #Get the request body in sring format
        body = request.body.decode('utf-8')
        #Parse the body as JSON
        json_data = json.loads(body)
        #Use the create "model" to create the record
        response = models.create(json_data, hash(json_data['Password']))
        id_ = response.inserted_id
    #Return the response
    return HttpResponse(models.user_trigger(id_))

#Put
#Updates a record or records
'''
Use the URL localhost:8000/users/ and following JSON to test:
{
	"bulk":"true",  
    "search_field":"Role",   
    "search_term":"User",   
    "update_field":"Role",   
    "update_value":"Manager",   
    "limit":2
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
#[localhost:8000/users?bulk=(true/false)] {"search_terms": {(key):(value)}}
'''
def delete(request):
    print("delete chosen")
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    bulk = json_data.get('bulk', "false")
    if bulk == "false":
        response = models.delete(json.loads(json_data['search_terms']))
        print("false")
    elif bulk == "true":
        response = models.bulk_delete(json.loads(json_data['search_terms']))
        print("true")
    else: 
        print("Delete did not work")
    return HttpResponse(response)
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

#Authenticate
#Allows a user to log in
#Parameters: username, password
#[localhost:8000/users/auth] {"username":"(username)", "password":"(password)"}
@csrf_exempt
def authenticate(request):
    if request.method == "GET":
        if request.session['auth']:
            return HttpResponse("true")
        else:
            return HttpResponse("false")
    else:
        #Get the request body in sring format
        body = request.body.decode('utf-8')
        json_data = json.loads(body)
        print(hash(json_data['Password']))
        response = models.authenticate(json_data['Username'], hash(json_data['Password']))
        #Return the response (true/false)
        return HttpResponse(response)
    
#Helper Functions
#Hash
#Hashes a string
#Parameters: string
def hash(string):
    return sha256(string.encode('utf-8')).hexdigest()