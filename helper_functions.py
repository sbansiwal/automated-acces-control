from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
from tools_api import *


access_token = "XXXXXXXXX"
verification_token = "XXXXXXXXXXX"

def check_interactive_message(payload):
    payload = loads(payload)
    user_id = payload["user"]["id"]
    
    if payload["actions"][0]["name"] == "github":
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": "Provide your github username with slash command as '/testcomment github $username'",
            "headers":  { }
        }
        
    if user_id == "U015UKJKXNW":
        return check_interactive_message_manager(payload)
    elif user_id == "U015QP5QHN0":
        return check_interactive_message_admin(payload)
    else:
        return check_interactive_message_user(payload)


def check_interactive_message_manager(payload):
    #payload = loads(payload)
    print(payload)
    
    if "type" in payload:
        if payload["type"] == "interactive_message":
            if payload["actions"][0]["name"] == "approve":
                if payload["actions"][0]["value"] == "jira":
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": "Jira access granted",
                        "headers":  { }
                    }
                elif payload["actions"][0]["value"] == "github":
                    request_admin(payload)
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": "Request forwarded to admin",
                        "headers":  { }
                    }
                else:
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": "Tool not specified",
                        "headers":  { }
                    }
            else:
                disapproval_message(payload["callback_id"], "Manager")
                return {
                    "isBase64Encoded": True,
                    "statusCode": 200,
                    "body": "Tool access disapproved",
                    "headers":  { }
                }
        else:
            return {
                "isBase64Encoded": True,
                "statusCode": 200,
                "body": "Not an interactive message",
                "headers":  { }
            }
    else:
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": "type field not present in payload",
            "headers":  { }
        }


def check_interactive_message_admin(payload):
    #payload = loads(payload)
    print(payload)
    
    if "type" in payload:
        if payload["type"] == "interactive_message":
            if payload["actions"][0]["name"] == "approve":
                if payload["actions"][0]["value"] == "jira":
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": "Jira access granted",
                        "headers":  { }
                    }
                elif payload["actions"][0]["value"] == "github":
                    github_handler(payload["original_message"]["attachments"][0]["fallback"], payload["original_message"]["attachments"][0]["callback_id"])
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": "Github access granted",
                        "headers":  { }
                    }
                else:
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": "Tool not specified",
                        "headers":  { }
                    }
            else:
                disapproval_message(payload["callback_id"], "Admin")
                return {
                    "isBase64Encoded": True,
                    "statusCode": 200,
                    "body": "Tool access disapproved",
                    "headers":  { }
                }
        else:
            return {
                "isBase64Encoded": True,
                "statusCode": 200,
                "body": "Not an interactive message",
                "headers":  { }
            }
    else:
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": "type field not present in payload",
            "headers":  { }
        }
        
        
def check_interactive_message_user(payload):
    #payload = loads(payload)
    print(payload)
    
    if "type" in payload:
        if payload["type"] == "interactive_message":
            if payload["actions"][0]["name"] == "github":
                request_manager(payload)
                return {
                    "isBase64Encoded": True,
                    "statusCode": 200,
                    "body": "Request sent to manager",
                    "headers":  { }
                }
            elif payload["actions"][0]["name"] == "jira":
                return {
                    
                }
            elif payload["actions"][0]["name"] == "sumologic":
                return {
                    
                }
            else:
                return {
                    "isBase64Encoded": True,
                    "statusCode": 200,
                    "body": "Tools not selected",
                    "headers":  { }
                }
        else:
            return {
                "isBase64Encoded": True,
                "statusCode": 200,
                "body": "Not an interactive message",
                "headers":  { }
            }
    else:
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": "type field not present in payload",
            "headers":  { }
        }
        
        
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
    print("json_response")
    print(json_response)
    

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
    print("json_response")
    print(json_response)
    
    return json_response
    
    
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
    print("json_response")
    print(json_response)
    
    
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
    print(json_response)