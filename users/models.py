from json import loads
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
def user(json_object):
    new_record = {}
    for key in json_object:
        new_record[key] = json_object[key]
    return new_record
#Get
#Returns a number of records equal to the limit
#Parameters: none
def get(limit):
    return coll.find().limit(limit)
#Create
#Creates a single new user
#Parameters: new user object
def create(new):
    return coll.insert_one(user(new))
#Bulk_create
#Creates multiple new users
#Parameters: array of new user objects
def bulk_create(new_array):
    object_list = []
    for new in new_array:
        object_list += user(new)
    return coll.insert_many(object_list)
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
def authenticate(terms):
    exists = coll.find(terms)
    if exists.count() > 0:
        return True
    else:
        return False