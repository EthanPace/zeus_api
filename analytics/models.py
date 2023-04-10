from json import loads
from bson.json_util import dumps
import pymongo

#Analytics:
#		- Tasks:
#			- Find the maximum precipitation recorded in the last 5 years (single)			
#		- Methods: 
#			- Get
#				- Input JSON: {field/column, aggregation}
#				- Output JSON {the aggregated data on the chosen column}

client = pymongo.MongoClient("mongodb+srv://testUser:testPassword@nasadata.dpq7x0s.mongodb.net/test")
db = client['weatherDataDB']
coll = db['weatherData']

#Get_aggregation
#Returns the aggregated data on the chosen column
#Parameters: field, aggregation
def get_aggregation(field, aggregation):
    if field == "precipitation":
        field = "Precipitation mm/h"
    #Aggregation pipeline
    pipeline = [
        {
            "$group": {
                "_id": "$your_grouping_field",
                "max_precipitation": { "$max": "$Precipitation mm/s" }
            }
        }
    ]
    #[
        #Filter out data before 2015
        #{ "$match": { "Time": { "$gte": "2015-01-01T00:00:00+10:00" } } },
        #Group by the aggregation
        #{ "$group": { "_id": "$" + field, "aggregation": { "$" + aggregation: "$" + field } } }
    #]
    #Return the aggregated data
    response = dumps(list(coll.aggregate(pipeline)))
    return response #Returns a cursor