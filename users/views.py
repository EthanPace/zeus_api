#Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps
from . import models
from hashlib import sha256

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
            hashes.append(hash(user['password']))
        #Use the create "model" to create the records
        response = models.bulk_create(json_data['users'], hashes)
        id_ = response.inserted_ids
    else:
        #Get the request body in sring format
        body = request.body.decode('utf-8')
        #Parse the body as JSON
        json_data = json.loads(body)
        #Use the create "model" to create the record
        response = models.create(json_data, hash(json_data['password']))
        id_ = response.inserted_id
    #Return the response
    return HttpResponse(models.user_trigger(id_))

#Put
#Updates a record or records
#Parameters: search_terms (record/array), new (record/array), bulk (boolean)
#[localhost:8000/users/] {}
def put(request):
    # Check content-type header
    content_type = request.META.get('CONTENT_TYPE')
    if content_type != 'application/json':
        return JsonResponse({'result': 'false'})

    # Get the request body in string format
    body = request.body.decode('utf-8')
    try: #Try to parse the body as JSON
        json_data = json.loads(body)
        print(json_data)
        #Check if the request is a bulk operation
        if 'bulk' in json_data:
            if json_data['bulk'] == "false": #If not bulk, update one record
                response = models.update(json_data['search_terms'], json_data['new'])
            elif json_data['bulk'] == "true": #If bulk, update multiple records
                response = models.bulk_update(json_data['search_terms'], json_data['new'])
        else: #By default, update one record
            response = models.update(json_data['search_terms'], json_data['new'])
    except: #If the body is not JSON, return false
        return JsonResponse({'result':'false'})
    #Return the response
    return HttpResponse(response)
#Delete
#Deletes a record or records
#Parameters: search_terms, bulk (boolean)
#[localhost:8000/users?bulk=(true/false)] {"search_terms": {(key):(value)}}
def delete(request):
    body = request.body.decode('utf-8')
    print("Body:", body)
    bulk = request.POST.get('bulk', "false")
    json_data = json.loads(body)
    print("json_data:", json_data)
    if bulk == "false":
        response = models.delete(json_data)
    elif bulk == "true":
        response = models.bulk_delete(json_data)
    return HttpResponse(response)

#Authenticate
#Allows a user to log in
#Parameters: username, password
#[localhost:8000/users/auth] {"username":"(username)", "password":"(password)"}
@csrf_exempt
def authenticate(request):
    #Get the request body in sring format
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    print(hash(json_data['password']))
    response = models.authenticate(json_data['username'], hash(json_data['password']))
    #Return the response (true/false)
    return HttpResponse(response)
    
#Helper Functions
#Hash
#Hashes a string
#Parameters: string
def hash(string):
    return sha256(string.encode('utf-8')).hexdigest()