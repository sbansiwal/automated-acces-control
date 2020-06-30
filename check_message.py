from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
from datetime import datetime
import string
from message_functions import *
from tools_api import *
from helper_functions import *
from database_api import *

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
    user_info = get_user_info(payload["original_message"]["attachments"][0]["callback_id"])
    user_profile = user_info["profile"]
    
    if "type" in payload:
        if payload["type"] == "interactive_message":
            if payload["actions"][0]["name"] == "approve":
                if payload["actions"][0]["value"] == "jira":
                    tool_access = check_record(user_profile["email"], "jira", "tool_status")
                    #tool_access = check_record("user12@test.com", "jira", "tool_status")

                    if tool_access == "no":
                        request_admin(payload)
                        message = "Request forwarded to admin"
                    else:
                        message = "Jira access already given"
                        
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": message,
                        "headers":  { }
                    }
                elif payload["actions"][0]["value"] == "github":
                    tool_access = check_record(user_profile["email"], "github", "tool_status")
                    #tool_access = check_record("usery@test.com", "github", "tool_status")
                    if tool_access == "no":
                        request_admin(payload)
                        message = "Request forwarded to admin"
                    else:
                        message = "GitHub access already given"
                        
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
                        "body": "Tool not listed under automated access control",
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
    user_info = get_user_info(payload["original_message"]["attachments"][0]["callback_id"])
    user_profile = user_info["profile"]
    
    admin_info = get_user_info(payload["user"]["id"])
    admin_profile = admin_info["profile"]
    
    if "type" in payload:
        if payload["type"] == "interactive_message":
            if payload["actions"][0]["name"] == "approve":
                if payload["actions"][0]["value"] == "jira":
                    tool_access = check_record(user_profile["email"], "jira", "tool_status")
                    #tool_access = check_record("user12@test.com", "jira", "tool_status")
                    print("tools access : ", tool_access)
                    
                    if tool_access == "no":
                        response = jira_handler(payload["original_message"]["attachments"][0]["callback_id"])
                        print(response)
                        
                        if "active" in response and response["active"] == True:
                            message = "Jira access granted"
                            update_fields = {
                                "active": "yes",
                                "approved_by": admin_profile["real_name"] ,
                                "approved_time": str(datetime.now())
                            }
                            #update_response = update_user_record("user12@test.com", "jira", update_fields)
                            update_response = update_user_record(user_profile["email"], "jira", update_fields)
                            print("update response: ", update_response)
                            
                            if update_response == "error updating":
                                message = "error adding access approval to database"
                        else:
                            message = "Jira access not granted due to some error"
                                
                    else:
                        message = "Jira access already given"
                    
                    return {
                        "isBase64Encoded": True,
                        "statusCode": 200,
                        "body": message,
                        "headers":  { }
                    }
                elif payload["actions"][0]["value"] == "github":
                    tool_access = check_record(user_profile["email"], "github", "tool_status")
                   # tool_access = check_record("usery@test.com", "github", "tool_status")
                    if tool_access == "no":
                        response = github_handler(payload["original_message"]["attachments"][0]["fallback"], payload["original_message"]["attachments"][0]["callback_id"])
                        
                        if "active" in response and response["active"] == True:
                            message = "GitHub access granted"
                            update_fields = {
                                "active": "yes",
                                "approved_by": admin_profile["real_name"] ,
                                "approved_time": datatime.now()
                            }
                            update_response = update_user_record(user_profile["email"], "github", update_fields)
                            if update_response == "error updating":
                                message = "error adding access approval to database"
                        else:
                            message = "GitHub access not granted due to some error"
                            
                    else:
                        message = "GitHub access already given"
                        
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
                        "body": "Tool not listed under automated access control",
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
    user_info = get_user_info(payload["user"]["id"])
    user_profile = user_info["profile"]
    
    if "type" in payload:
        if payload["type"] == "interactive_message":
            
            if payload["actions"][0]["name"] == "github":
                request_details = {
                    "email": user_profile["email"],
                    "id": get_random_alphaNumeric_string(),
                    "name": user_profile["real_name"],
                    "tool": "github" 
                }
                response = add_user(request_details)
                
                if response == "error adding":
                    message = "Error adding request to database"
                else:
                    message = "Request forwarded to manager for github access"
                    request_manager(payload)
                    
                return {
                    "isBase64Encoded": True,
                    "statusCode": 200,
                    "body": message,
                    "headers":  { }
                }
            elif payload["actions"][0]["name"] == "jira":
                request_details = {
                    "email": user_profile["email"],
                    #"email": "user12@test.com",
                    "id": get_random_alphaNumeric_string(),
                    #"name": "testuser12",
                    "name": user_profile["real_name"],
                    "tool": "jira" 
                }
                response = add_user(request_details)
            
                if response == "error adding":
                    message = "Error adding request to database"
                else:
                    message = "Request forwarded to manager for jira access"
                    request_manager(payload)
                    
                return {
                    "isBase64Encoded": True,
                    "statusCode": 200,
                    "body": message,
                    "headers":  { }
                }
            elif payload["actions"][0]["name"] == "sumologic":
                request_details = {
                    "email": user_profile["email"],
                    "id": get_random_alphaNumeric_string(),
                    "name": user_profile["real_name"],
                    "tool": "sumologic" 
                }
                response = add_user(request_details)
                
                if response == "error adding":
                    message = "Error adding request to database"
                else:
                    message = "Request forwarded to manager for sumologic access"
                    request_manager(payload)
                    
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
    
