from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
import random
import string

access_token = "xoxb-XXXXXXXXXX"
verification_token = "XXXXXXXXXXXX"


def get_random_alphaNumeric_string(stringLength=20):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


# To get user info from the user_id 
def get_user_info(user_id):
    url = "https://slack.com/api/users.profile.get?user=" + user_id
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " + access_token
    }
    
    response = requests.request(
      "GET",
      url,
      headers=headers
    )
    
    response = dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    json_response = loads(response)
    return json_response     


def check_response(response, tool):
    if tool == "jira":
        if "errorMessages" in response:
            return "error"
        elif "active" not in response or response["active"] == False:
            return "inactive"
    elif tool == "github":
        if "message" in response:
            return "error"
    
    return "correct"  
    
    
def response_message(message):
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": message,
        "headers":  { }
    }
    
    
def nil_response():
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": ""
    }


def tool_request_details(email, name, tool):
    return {
        "email": email,
        "id": get_random_alphaNumeric_string(),
        "name": name,
        "tool": tool
    }
    
    
def update_fields_json(active_status, admin_name, datetime):
    return {
        "active": active_status,
        "approved_by": admin_name,
        "approved_time": datetime
    }
    
    
def post_response(user_id, message):
    user_info = get_user_info(user_id)
    user_profile = user_info["profile"]
    
    url = "https://slack.com/api/chat.postMessage"
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    
    data = {
        "channel": user_id,
        "attachments": [
            {
                "text": message,
                "color": "#3AA3E3"
            }
        ]
    }
    
    response = requests.request(
        "POST", 
        url,
        headers = headers, 
        data = dumps(data)
    )
    
    response = dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    json_response = loads(response)
    #print(json_response)
    #return json_response
    return
    
    