from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth

# get user record from primary key
def get_user_record(key):
    url = "https://6f0c74c99f79.ngrok.io/get/" + key
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
    }
    
    response = requests.request(
        "GET", 
        url,
        headers = headers
    )
    
    response = dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    json_response = loads(response)
    #print(json_response)
    return json_response
    
# add user record in database    
def add_user(body):
    record_present = check_record(body["email"], body["tool"], "is_present")
    
    if record_present == "yes":
        return "error adding"
        
    url = "https://6f0c74c99f79.ngrok.io/add"
    
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
    }
    
    data = body
    
    response = requests.request(
        "POST",
        url,
        headers = headers,
        data = dumps(data)
    )
    
    return response.text
    
# update user record in the database    
def update_user_record(email, tool, body):
    id_response = check_record(email, tool, "get_id")
    
    if id_response == "Tunnel error":
        return id_response
        
    url = "https://6f0c74c99f79.ngrok.io/update"
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
    }
    
    data = {
        "id": id_response,
        "active": body["active"],
        "approved_by": body["approved_by"],
        "approved_time": body["approved_time"],
    }
    
    response = requests.request(
        "POST",
        url,
        headers = headers,
        data = dumps(data)
    )
    
    return response.text

# check user record for tool access status
def check_record(email, tool, purpose):
    url = "https://6f0c74c99f79.ngrok.io/check"
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
    }
    
    data = {
        "email": email,
        "tool": tool
    }
    
    response = requests.request(
        "GET",
        url,
        headers = headers,
        data = dumps(data)
    )
    
    if response.text == "Tunnel 6f0c74c99f79.ngrok.io not found":
        return "Tunnel error"
    
    print(response.text)
    
    response = dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    json_response = loads(response)
    
    if purpose == "tool_status":
        if "active" in json_response:
            return json_response["active"]
        else:
            "response_error"
    elif purpose == "get_id":
        if "id" in json_response:
            return json_response["id"]
        else:
            return "response_error"
    else:
        if "name" in json_response:
            return "yes"
        else:
            return "no"

# get tool access list    
def get_access_list():
    url = "https://6f0c74c99f79.ngrok.io/list"
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
    }
    
    response = requests.request(
        "GET",
        url,
        headers = headers
    )
    
    response = dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    json_response = loads(response)
    return json_response

    