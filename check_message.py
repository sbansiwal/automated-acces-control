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

# checks the interactive message response from the user        
def check_interactive_message_user(payload):
    user_info = get_user_info(payload["user"]["id"])
    user_profile = user_info["profile"]
    tool = payload["actions"][0]["name"]
    
    request_details = tool_request_details("test2@gmail.com", "testuser2", tool)
    #response = add_user(request_details)
    response = "pass"
    
    if response == "error adding" or response == "Tunnel error":
        message = "Error adding request to database"
    else:
        message = "Request forwarded to <@" + "U015UKJKXNW>" + " for `" + payload["actions"][0]["name"] + "` access"
        request_manager(payload)
        
    return response_message(message)
       
       
# checks the interactive message response from manager
def check_interactive_message_manager(payload):
    user_id = payload["original_message"]["attachments"][0]["callback_id"]
    user_info = get_user_info(user_id)
    user_profile = user_info["profile"]
    tool = payload["actions"][0]["value"]
    
    if payload["actions"][0]["name"] == "approve":
        #tool_access = check_record(user_profile["email"], "jira", "tool_status")
        #tool_access = check_record("test2@gmail.com", tool, "tool_status")
        tool_access = "no"
        
        if tool_access == "no":
            request_admin(payload)
            message = "Request forwarded to <@" + "U015QP5QHN0>" + " for `" + tool + "` access request by <@" + user_id + ">"
        else:
            message = "`" + tool + "` access already given to <@" + user_id + ">"
            
        return response_message(message)
    else:
        disapproval_message(payload["callback_id"], "Manager", tool)
        message = "`" + tool + "` access request by <@" + user_id + "> disapproved"
        return response_message(message)
        
        
# checks the interactive message response from the admin
def check_interactive_message_admin(payload):
    user_id = payload["original_message"]["attachments"][0]["callback_id"]
    user_info = get_user_info(user_id)
    user_profile = user_info["profile"]
    tool = payload["actions"][0]["value"]
    
    admin_info = get_user_info(payload["user"]["id"])
    admin_profile = admin_info["profile"]
    
    
    if payload["actions"][0]["name"] == "approve":
        #tool_access = check_record(user_profile["email"], "jira", "tool_status")
        tool_access = check_record("test1@gmail.com", tool, "tool_status")
        print("check admin, tool access : ", tool_access)
        tool_access = "no"
        
        if tool_access == "no":
            update_fields = update_fields_json("yes", admin_profile["real_name"], str(datetime.now()))
            update_response = update_user_record("test2@gmail.com", tool, update_fields)
            
            if tool == "jira":
                response = jira_handler(user_id)
            elif tool == "github":
                response = github_handler(payload["original_message"]["attachments"][0]["fallback"], payload["original_message"]["attachments"][0]["callback_id"])
            
            response_result = check_response(response, tool)
            
            if response_result == "error":
                message = "error giving `" + tool + "` access to <@" + user_id + ">"
                return response_message(message)
            elif response_result == "inactive":
                message = "`" + tool + "` access not active from request by <@" + user_id + ">"
                return response_message(message)
            else:
                message = "`" + tool + "` access granted to <@" + user_id + ">"
                update_fields = update_fields_json("yes", admin_profile["real_name"], str(datetime.now()))
                update_response = update_user_record("suniltest@test.com", tool, update_fields)
                #update_response = update_user_record(user_profile["email"], payload["actions"][0]["value"], update_fields)
                
                if update_response == "error updating":
                    message = "error adding access approval to database for `" + tool + "` access request by  <@" + user_id + ">"
                
                return response_message(message) 
        else:
            message = "`" + tool + "` access already given to <@" + user_id + ">"
        
        return response_message(message)
    else:
        disapproval_message(payload["callback_id"], "Admin", tool)
        message = "`" + tool + "` access request by <@" + user_id + "> disapproved"
        return response_message(message)


