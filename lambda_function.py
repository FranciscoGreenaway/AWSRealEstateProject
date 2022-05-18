from S3_Handler import upload_to_S3
import requests
import json
import urllib.request
import state_abbr_dict
import pandas as pd
from pandas.io.json import json_normalize
from io import StringIO
import boto3

def lambda_handler(event, context):

    # Property Search API call/Load into S3 object
    property_search_buffer = property_search()
    upload_to_S3.put_object_S3(property_search_buffer, file_name=f'property_search/properties-for-sale-{location.split(",")[0]}-{location.split(",")[1].strip()}.csv')

    # # Postal Address API to retrieve county
    get_county_from_address()
    get_state()

    # Get declared disaster data of the location/Load into S3 object
    disasters = disaster_declarations()
    upload_to_S3.put_object_S3(disasters, file_name=f'disasters/disaster_declarations-{location.split(",")[0]}-{location.split(",")[1].strip()}.csv')


def property_search():

    # Make sure you abbreviate the state in the location variable
    global location
    location = "lehigh acres, fl"

    status_type = "ForSale"
    home_type = "Houses, multi-family"
    sort = "ForSale"
    max_price = 300000

    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

    querystring = {
        "location":location,
        "status_type":status_type,
        "home_type":home_type,
        "sort":sort,
        "maxPrice":max_price
    }

    headers = {
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com",
        "X-RapidAPI-Key": "7f53f2b755msh1dde51426995797p143ccejsn1d591daa1ac5"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    property_search_response_JSON = response.json()

    df_properties = json_normalize(property_search_response_JSON['props'])

    csv_buffer = StringIO()
    df_properties.to_csv(csv_buffer, encoding='utf-8', index=False)

    return csv_buffer


# API request to retrieve the county of an address
def get_county_from_address():
    global county

    url = "http://www.yaddress.net/api/address"

    querystring = {
        "AddressLine2": location
    }
    headers = {
        "Accept": "application/json"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    county_response_JSON = response.json()

    county = county_response_JSON['County']


def get_state():
    # Split location variable on comma to access state
    global state
    state = location.split(",")[1].strip().upper()

    if len(state) != 2:
        get_state_abbr()


def get_state_abbr():
    for k, v in state_abbr_dict.us_state_to_abbrev.items():
        if k == state.capitalize():
            state = state_abbr_dict.us_state_to_abbrev[state]


def disaster_declarations():
    base_url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?"

    web_url = urllib.request.urlopen(base_url + f"$select=state,declarationDate,incidentType,disasterNumber"
                                                f",declarationTitle,incidentBeginDate,designatedArea,placeCode,id"
                                                f"&$filter=state%20eq%20%27{state}%27%20and%20designatedArea"
                                                f"%20eq%20%27{county.capitalize()}%20(County)%27%20"
                                                f"and%20incidentBeginDate%20gt%20%272010-01-01T00:00:00.000Z%27&"
                                     )

    results = web_url.read()
    disaster_declarations_JSON = json.loads(results.decode())


    df_disasters = json_normalize(disaster_declarations_JSON['DisasterDeclarationsSummaries'])

    csv_buffer_dd = StringIO()
    df_disasters.to_csv(csv_buffer_dd, encoding='utf-8', index=False)

    return csv_buffer_dd


