from json import loads
from bson.json_util import dumps
import pymongo
from bson.objectid import ObjectId
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# TO DO:
#     - Check that methods are standardized across apps (least important)

# Create your models here.
client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test&tls=true")
db = client['weatherDataDB']
coll = db['users']

#User
#"Model" for the user object
def user(username, password, other_keys):
    new_record = {}
    for key in other_keys:
        new_record[key] = other_keys[key]
    new_record['Username'] = username
    new_record['Password'] = password
    return new_record

#Get
#Returns a number of records equal to the limit
#Parameters: none
def get(limit):
    return coll.find().limit(limit)

#Find
#Returns one record that matches the search terms
#Parameters: search terms
#def find(search_terms):
#    return coll.find_one(search_terms)
def find(search = "", limit = 10):
    if search == "":
        return coll.find().limit(limit)
    else:
        return coll.find({"_id":ObjectId(search)}).limit(limit)
    
#Create
#Creates a single new user
#Parameters: new user object
def create(keys, hashed_password):
    return coll.insert_one(user(keys['Username'], hashed_password, keys))

#Bulk_create
#Creates multiple new users
#Parameters: array of new user objects
def bulk_create(keys, hashed_passwords):
    cursors = []
    for i in range(len(keys)):
        curs = coll.insert_one(user(keys[i]['Username'], hashed_passwords[i], keys[i]))
        cursors.append(curs)
    return cursors

#Update
#Updates a single user
#Parameters: search terms, update object
def update(search_terms, new):
    return coll.update_one(search_terms, new)

#Bulk_update
#Updates multiple users
#Parameters: search terms, update array
def bulk_update(query, update, limit = None):
    if limit == None:
        return coll.update_many(query, update)
    else:
        try:
            cursor = coll.find(query).limit(limit)
            for document in cursor:
                coll.update_one({"_id":document["_id"]}, update)
            return {"results": "success"}
        except:
            return {"results": "fail"}

#Delete
#Deletes a single user
#Parameters: search terms
def delete(search_terms):
    return coll.delete_one(search_terms)

#Bulk_delete
#Deletes multiple users
#Parameters: search terms
def bulk_delete(search_terms):
    return coll.delete_many(search_terms)

#Authenticate
#Authenticates a user
#Parameters: username, password
def authenticate(username, password):
    exists = coll.count_documents({"Username":username,"Password":password})
    print(exists)
    if exists > 0:
        return True
    else:
        return False
    
#Trigger
#Forces a user to have a permission level on creation
#Parameters: id
def user_trigger(id_):
    print (id_)
    if str(id_):
        cursor = coll.find_one({"_id":id_})
        if cursor.get('permissions', None) == None:
            for document in cursor:
                coll.update_one({"_id":id_}, {"$set":{"permissions":"public"}})
            return ("Updated permissions for user " + str(id_))
        else:
            return ("Permissions already set for user " + str(id_))
    else:
        return ("No user found")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)