from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
from message_functions import *
from tools_api import *

# to check if the interactive message is from user, manager or admin
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

# checks the interactive message response from manager
def check_interactive_message_manager(payload):
    #payload = loads(payload)
    #print(payload)
    
    if "type" in payload:
        if payload["type"] == "interactive_message":
            if payload["actions"][0]["name"] == "approve":
                if payload["actions"][0]["value"] == "jira":
                    request_admin(payload)
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": "Request forwarded to admin",
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


# checks the interactive message response from the admin
def check_interactive_message_admin(payload):
    #payload = loads(payload)
    #print(payload)
    
    if "type" in payload:
        if payload["type"] == "interactive_message":
            if payload["actions"][0]["name"] == "approve":
                if payload["actions"][0]["value"] == "jira":
                    response = jira_handler(payload["original_message"]["attachments"][0]["callback_id"])
                    if response["active"] == "true":
                        message = "Jira access granted"
                        
                    else:
                        message = "Jira Access not granted due to some error"
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": message,
                        "headers":  { }
                    }
                elif payload["actions"][0]["value"] == "github":
                    response = github_handler(payload["original_message"]["attachments"][0]["fallback"], payload["original_message"]["attachments"][0]["callback_id"])
                    if response["active"] == "true":
                        message = "GitHub access granted"
                    else:
                        message = "Github Access not granted due to some error"
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": message,
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
        

# checks the interactive message response from the user        
def check_interactive_message_user(payload):
    #payload = loads(payload)
    #print(payload)
    
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
                request_manager(payload)
                return {
                    "isBase64Encoded": True,
                    "statusCode": 200,
                    "body": "Request sent to manager",
                    "headers":  { }
                }
            elif payload["actions"][0]["name"] == "sumologic":
                return {
                    "isBase64Encoded": True,
                    "statusCode": 200,
                    "body": "Request sent to manager",
                    "headers":  { }    
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
    
