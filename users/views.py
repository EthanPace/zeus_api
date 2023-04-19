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
    elif(request.method == "OPTIONS"):
        return options(request)

#Get
#Returns ten records (default), or a specified number of records, or a specific record based on search terms
#Parameters: none
def get(request):
    query = request.GET
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
    else:
        #Get the request body in sring format
        body = request.body.decode('utf-8')
        #Parse the body as JSON
        json_data = json.loads(body)
        #Use the create "model" to create the record
        response = models.create(json_data, hash(json_data['Password']))
        models.user_trigger(response.inserted_id)
    #Return the response
    return HttpResponse(200)

#Put
#Updates a record or records
#[localhost:8000/users/]
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
#Parameters: oid (record id), bulk (boolean), search_terms (dictionary)
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

#Authenticate
#Allows a user to log in
#Parameters: username, password
#[localhost:8000/users/auth] {"username":"(username)", "password":"(password)"}
@csrf_exempt
def authenticate(request):
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

'''
BELOW METHOD WAS PULLED FROM YOUTUBE VIDEO, CURRENTLY JUST FOR REFERENCE, 
WOULD NOT WORK IN THIS PROJECT DUE TO NOT USING BUILT IN DATABASE
@api_view(['POST',])
def registation_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
'''