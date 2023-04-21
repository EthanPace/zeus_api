from django.test import TestCase

# Create your tests here.

# GET /search
'''
localhost:8000/stations/?id=dlb_atm41_5282
'''

# POST 1
'''
{
    "bulk": "false",
    "new": [
            {
                "_id": "dlb-atm-41-5281",
                "Device Name": "DLB ATM41 Speers Point Pool",
                "State": "NSW",
                "Latitude": "-32.96305",
                "Longitude": "151.61993",
                "Last Response": ""
            }
            ]
}
'''

# PUT 1
'''
{
  "bulk": "false",
  "search_field":"Device Name", "search_term":"DLB ATM41 Charlestown Skate Park", "update_field":"Device Name", "update_value":"DLB ATM41 Possibly Charlestown Skate Park", "limit":100
}
'''

# PATCH
'''
def patch(request):
    body = request.body.decode('utf-8')
    try:
        json_data = json.loads(body)
        if 'bulk' in json_data:
            if json_data['bulk'] == "false":
                response = models.update(json_data['search_terms'], json_data['new'])
            elif json_data['bulk'] == "true":
                response = models.bulk_update(json_data['search_terms'], json_data['new'])
        else:
            response = models.update(json_data['search_terms'], json_data['new'])
    except:
        return HttpResponse("false")
    return HttpResponse(response)
'''

# DELETE 1
'''
{
  "bulk": "false",
  "search_terms":
  {
      "Device Name": "Dummy Station"
  }
}
'''