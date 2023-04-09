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
    else:
        #Get the request body in sring format
        body = request.body.decode('utf-8')
        #Parse the body as JSON
        json_data = json.loads(body)
        #Use the create "model" to create the record
        response = models.create(json_data, hash(json_data['password']))
    #Return the response
    return HttpResponse(response)

#Put
#Updates a record or records
#Parameters: search_terms, new (record/array), bulk (boolean)
def put(request):
    #Get the request body in sring format
    body = request.body.decode('utf-8')
    try: #Try to parse the body as JSON
        json_data = json.loads(body)
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
def delete(request):
    body = request.body.decode('utf-8')
    bulk = request.POST.get('bulk', "false")
    json_data = json.loads(body)
    if bulk == "false":
        response = models.delete(json_data)
    elif bulk == "true":
        response = models.bulk_delete(json_data)
    return HttpResponse(response)
#Authenticate
#Allows a user to log in
#Parameters: username, password
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
        print(hash(json_data['password']))
        response = models.authenticate(json_data['username'], hash(json_data['password']))
        if response:
            request.session['auth'] = True
            request.session['perms'] = models.get_perms(json_data['username'])
        else:
            request.session['auth'] = False
            request.session['perms'] = None
        #Return the response (true/false)
        return HttpResponse(response)
#Logout
#Allows a user to log out
#Parameters: none
@csrf_exempt
def logout(request):
    request.session['auth'] = False
    request.session['perms'] = None
    return HttpResponse("true")
#Helper Functions
#Hash
#Hashes a string
#Parameters: string
def hash(string):
    return sha256(string.encode('utf-8')).hexdigest()