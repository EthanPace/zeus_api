from json import loads
from bson.json_util import dumps
import pymongo
from bson.objectid import ObjectId

# TO DO:
#     - Test delete functionality, singular and bulk [localhost:8000/users?bulk=(true/false)] {"search_terms": {"username": "(username)"}}
#     - Test update functionality, singular and bulk [localhost:8000/users/] {"bulk":"true/false", "search_terms": {(key):(value)}, "new": {(key):(value)}}
#     - Test authentication functionality [localhost:8000/users/auth] {"username":"(username)", "password":"(password)"}
#     - Add trigger to Atlas to update last logged in field
#     - Remove long comment in this file (below)
#     - Check that methods are standardized across apps (least important)
# Users:
# 		- Tasks:
# 			- Insert a new user (single) -- DONE
# 			- Delete a user (single) -- BROKEN (Gives 301 code and doesnt delete)
# 			- Delete multiple users (multiple) -- BROKEN (Gives 301 code and doesnt delete)
# 			- Update access level for at least two users in the same query (multiple) -- UNSURE
			
# 		- Methods: 			
# 			- Post:
# 				- Input JSON: {1 new user object} -- DONE
# 				- Output JSON: {success / fail} -- DONE

# 				- Input JSON: {Multiple new user object} -- DONE
# 				- Output JSON: {success / fail} -- DONE
				
			
# 			- PUT: -- 
# 				- Input JSON: {new access levels for at least 2 users (in the same query)} -- DONE
# 				- Output JSON: {success / fail} -- DONE
# 			- DELETE:
# 				- Input JSON: {Single user} -- NOT WORKING, GIVES 301 CODE AND DOESNT DELETE
					
# 				- Input JSON: {Multiple users) -- TO DO (BROKEN)

# 		- Trigger:
# 			- Configure last logged in trigger in atlas -- DONE
#           - Assign role to public if isn't admin or manager?	-- DONE	
# 		- Secondary endpoint:
# 			- Authenticate	
# 				- Methods: 			
# 					- GET: 
# 						- Input JSON: {username + password} -- DONE
# 						- Output JSON: {if authenticated}} -- DONE

# Create your models here.
client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test")
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
