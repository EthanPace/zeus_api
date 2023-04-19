from django.test import TestCase


#Get
#Returns ten records (default), or a specified number of records, or a specific record based on search terms
#Parameters: none
'''
localhost:8000/users/?oid=6438b6f43e10290d0c088ebf
'''
#Post
#Creates a new record or records
#Parameters: new (record/array), bulk (boolean)
#[localhost:8000/users/] {"bulk":"true/false", "users": [{"username":"(username)", "password":"(password)"}, {"username":"(username)", "password":"(password)"}]}
'''
{
  "bulk": "true",
  "new": [
    {
      "Time": "2022-01-01T00:00:00+00:00",
      "Device ID": "dlb-atm41-0001",
      "Device Name": "DLB ATM41 Test Device 1",
      "Latitude": 45.123456,
      "Longitude": -122.123456,
      "Temperature (\u00b0C)": 20.5,
      "Atmospheric Pressure (kPa)": 101.325,
      "Lightning Average Distance (km)": 0.0,
      "Lightning Strike Count": 0.0,
      "Maximum Wind Speed (m/s)": 2.0,
      "Precipitation mm/h": 0.0,
      "Solar Radiation (W/m2)": 0.0,
      "Vapor Pressure (kPa)": 2.0,
      "Humidity (%)": 60.0,
      "Wind Direction (\u00b0)": 180.0
    },
    {
      "Time": "2022-01-02T00:00:00+00:00",
      "Device ID": "dlb-atm41-0002",
      "Device Name": "DLB ATM41 Test Device 2",
      "Latitude": 45.654321,
      "Longitude": -122.654321,
      "Temperature (\u00b0C)": 18.0,
      "Atmospheric Pressure (kPa)": 101.0,
      "Lightning Average Distance (km)": 0.0,
      "Lightning Strike Count": 0.0,
      "Maximum Wind Speed (m/s)": 1.5,
      "Precipitation mm/h": 0.0,
      "Solar Radiation (W/m2)": 0.0,
      "Vapor Pressure (kPa)": 1.8,
      "Humidity (%)": 70.0,
      "Wind Direction (\u00b0)": 270.0
    }
  ]
}
'''
#Put
#Updates a record or records
#[localhost:8000/users/]
'''
{
    "bulk":"true", 
    "search_field":"Role", 
    "search_term":"Manager", 
    "update_field":"Role", 
    "update_value":"Admin", 
    "limit":1
}
'''
#Delete
#Deletes a record or records
#Parameters: oid (record id), bulk (boolean), search_terms (dictionary)
'''
{
    "oid": "6438b6f43e10290d0c088ebe"
}
'''
#Authenticate
#Allows a user to log in
#Parameters: username, password
#[localhost:8000/users/auth] {"username":"(username)", "password":"(password)"}
'''
{"username":"bhund", "password":"bhund123!"}
'''