from django.db import models

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
