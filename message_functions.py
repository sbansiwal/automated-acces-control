from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
from helper_functions import *

access_token = "XXXXXXXXXXXXXX"
verification_token = "XXXXXXXXXXXXXX"

# sends the tools to user after he requests them using slash command
def send_tools_user(user_id):    
    user_info = get_user_info(user_id)
    user_profile = user_info["profile"]
    print(user_profile)
    
    url = "https://slack.com/api/chat.postMessage"
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    
    data = {
        "channel": user_id,
        "text": "Hi " + user_profile["real_name"],
        "attachments": [
            {
                "text": "Which tool's access do you need?",
                "fallback": "Shame... buttons aren't supported in this land",
                "callback_id": user_id,
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "github",
                        "text": "GitHub",
                        "type": "button",
                        "value": "github",
                        "style": "default"
                    },
                    {
                        "name": "jira",
                        "text": "JIRA",
                        "type": "button",
                        "value": "jira",
                        "style": "defaul"
                    },
                    {
                        "name": "sumologic",
                        "text": "Sumo Logic",
                        "type": "button",
                        "value": "sumologic",
                        "style": "default"
                    }
                ]
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
    
    if "error" in json_response:
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": "Error occured",
            "headers": { }
        }
    else:
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "headers": { }
        }


# sends the tool access request by the user to manager          
def request_manager(payload):
    manager_info = get_user_info("U015UKJKXNW")
    manager_profile = manager_info["profile"]
    
    user_info = get_user_info(payload["user"]["id"])
    user_profile = user_info["profile"]
    
    accessTool = payload["actions"][0]["name"]
    url = "https://slack.com/api/chat.postMessage"
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    
    data = {
        "channel": "U015UKJKXNW",
        "text": "Hi " + manager_profile["real_name"],
        "attachments": [
            {
                "text": user_profile["real_name"] + " wants " + payload["actions"][0]["name"] + " access",
                "fallback": "Shame... buttons aren't supported in this land",
                "callback_id": payload["user"]["id"],
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "approve",
                        "text": "Approve",
                        "type": "button",
                        "value": accessTool,
                        "style": "primary"
                    },
                    {
                        "name": "disapprove",
                        "text": "Disapprove",
                        "type": "button",
                        "value": accessTool,
                        "style": "danger"
                    }
                ]
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
    return json_response
    

# sends the tool access request to manager if the access requires other user details
def request_manager_by_text(user_id, words):    
    manager_info = get_user_info("U015UKJKXNW")
    manager_profile = manager_info["profile"]
    
    user_info = get_user_info(user_id)
    user_profile = user_info["profile"]
    
    accessTool = words[0]
    username = words[1]
    
    url = "https://slack.com/api/chat.postMessage"
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    
    data = {
        "channel": "U015UKJKXNW",
        "text": "Hi " + manager_profile["real_name"],
        "attachments": [
            {
                "text": user_profile["real_name"] + " wants " + accessTool + " access",
                "fallback": username,
                "callback_id": user_id,
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "approve",
                        "text": "Approve",
                        "type": "button",
                        "value": accessTool,
                        "style": "primary"
                    },
                    {
                        "name": "disapprove",
                        "text": "Disapprove",
                        "type": "button",
                        "value": accessTool,
                        "style": "danger"
                    }
                ]
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
    return json_response
    

# sends the tool access request by the user to admin     
def request_admin(payload):
    admin_info = get_user_info("U015QP5QHN0")
    admin_profile = admin_info["profile"]
    
    user_id = payload["original_message"]["attachments"][0]["callback_id"]
    username = payload["original_message"]["attachments"][0]["fallback"]
    message = payload["original_message"]["attachments"][0]["text"]
    url = "https://slack.com/api/chat.postMessage"
    
    accessTool = payload["actions"][0]["value"]
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    
    data = {
        "channel": "U015QP5QHN0",
        "text": "Hi " + admin_profile["real_name"],
        "attachments": [
            {
                "text": message,
                "fallback": username,
                "callback_id": user_id,
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "approve",
                        "text": "Approve",
                        "type": "button",
                        "value": accessTool,
                        "style": "primary"
                    },
                    {
                        "name": "disapprove",
                        "text": "Disapprove",
                        "type": "button",
                        "value": accessTool,
                        "style": "danger"
                    }
                ]
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
    return json_response
    

# sends the disapproval message to user if manager/admin disapproves tool access request
def disapproval_message(user_id, user_type):
    url = "https://slack.com/api/chat.postMessage"
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    
    data = {
        "channel": user_id,
        "text": user_type + " has disapproved your request"
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
    return json_response        
       