#Imports
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson.json_util import dumps
from . import models
#Global Variables
logged_in = False
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
    #Use the create "model" to create the record
    response = models.create(json_data)
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
    #Get the request body in sring format
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    response = models.authenticate(json_data['name'], json_data['password'])
    if(response == "true"):
        logged_in = True
    else:
        logged_in = False
    #Return the response (true/false)
    return HttpResponse(response)