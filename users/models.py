from json import loads
from bson.json_util import dumps
import pymongo

# Users:
# 		- Tasks:
# 			- Insert a new user (single)
# 			- Delete a user (single)
# 			- Delete multiple users (multiple)
# 			- Update access level for at least two users in the same query (multiple)
			
# 		- Methods: 			
# 			- Post:			
# 				- Input JSON: {1 new user object}
# 				- Output JSON: {success / fail}

# 				- Input JSON: {Multiple new user object}
# 				- Output JSON: {success / fail}
				
			
# 			- PUT:
# 				- Input JSON: {new access levels for at least 2 users (in the same query)}
# 				- Output JSON: {success / fail}
# 			- DELETE:
# 				- Input JSON: {Single user}
					
# 				- Input JSON: {Multiple users)
# 		- Trigger:
# 			- Configure last logged in trigger in atlas 	
#           - Assign role to public if isn't admin or manager?		
# 		- Secondary endpoint:
# 			- Authenticate	
# 				- Methods: 			
# 					- GET:
# 						- Input JSON: {username + password}
# 						- Output JSON: {if authenticated}}

# Create your models here.
client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test")
db = client['weatherDataDB']
coll = db['employees']
#User
#"Model" for the user object
def user(username, password, other_keys):
    new_record = {}
    for key in other_keys:
        new_record[key] = other_keys[key]
    new_record['username'] = username
    new_record['password'] = password
    return new_record
#Get
#Returns a number of records equal to the limit
#Parameters: none
def get(limit):
    return coll.find().limit(limit)
#Find
#Returns one record that matches the search terms
#Parameters: search terms
def find(search_terms):
    return coll.find_one(search_terms)
#Create
#Creates a single new user
#Parameters: new user object
def create(keys, hashed_password):
    return coll.insert_one(user(keys['username'], hashed_password, keys))
#Bulk_create
#Creates multiple new users
#Parameters: array of new user objects
def bulk_create(keys, hashed_passwords):
    cursors = []
    for i in range(len(keys)):
        curs = coll.insert_one(user(keys[i]['username'], hashed_passwords[i], keys[i]))
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
def bulk_update(search_terms, new_array):
    return_list = []
    for new in new_array:
        for search_term in search_terms:
            return_list += coll.update_one(search_term, user(new))
    return return_list
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
    exists = coll.count_documents({"username":username,"password":password})
    print(exists)
    if exists > 0:
        return True
    else:
        return False
#Get_Perms
#Gets the permissions of a user
#Parameters: username
def get_perms(username):
    cursor = coll.find_one({"username":username})
    user_object = loads(dumps(list(cursor)[0]))
    return user_object['permissions']

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


