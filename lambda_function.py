from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
from message_functions import *
from check_message import check_interactive_message
from database_api import *

####### check update_user_record in check_interactive_message_admin  ###### .    
        
access_token = "xoxb-XXXXX-XXXXX-XXXXXX"
verification_token = "XXXXXXXXXXXXX"

# This is the lambda function. All the events triggered through the API are executed here
def lambda_handler(event, context):
    slack_payload = dict(urlparse.parse_qsl(event["body"]))

    if "payload" in slack_payload:
        return check_interactive_message(slack_payload["payload"])
    elif "text" not in slack_payload:
        return send_tools_user(slack_payload["user_id"])    
    else:
        slack_message = slack_payload["text"]
        words = slack_message.split(' ')
        return forward_request(slack_payload["user_id"], words)

def forward_request(user_id, words):
    response = request_manager_by_text(user_id, words)
    if response == "error adding":
        message = "Error adding request to database"
    else:
        message = "Request forwarded to manager"
        
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": message,
        "headers": { }
    }

# A dummy lambda handler
def lambda_handler_2(event, context):
    slack_payload = dict(urlparse.parse_qsl(event["body"]))
    #print(slack_payload)
    
    if "payload" in slack_payload:
        return check_interactive_message(slack_payload["payload"])
        
    if "text" not in slack_payload:
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": dumps("No text"),
            "headers": { }
        }
    
    slack_message = slack_payload["text"]
    words = slack_message.split(' ')
    
    return random_event(event, words)
    
    if words[0] == "Jira":
        return jira_handler(words)
    elif words[0] == "Github":
        return github_handler(words)
    else:
        return random_event(event, words)
    
    
