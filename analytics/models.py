from json import loads
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
    #Aggregation pipeline
    pipeline = [
        #Filter out data before 2015
        { "$match": { "Date": { "$gte": "2015-01-01" } } },
        #Group by the aggregation
        { "$group": { "_id": None, "max_precipitation": { aggregation: "$" + field } } }
    ]
    #Return the aggregated data
    return coll.aggregate(pipeline) #Returns a cursor