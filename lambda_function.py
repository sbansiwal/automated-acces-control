from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
from tools_api import *
from helper_functions import *


access_token = "XXXXXXXXXX"
verification_token = "XXXXXXXXX"


def lambda_handler(event, context):
    slack_payload = dict(urlparse.parse_qsl(event["body"]))
    print(slack_payload)
    if "payload" in slack_payload:
        return check_interactive_message(slack_payload["payload"])
    elif "text" not in slack_payload:
        return send_tool_buttons(slack_payload["user_id"])    
    else:
        slack_message = slack_payload["text"]
        words = slack_message.split(' ')
        return forward_request(slack_payload["user_id"], words)


def forward_request(user_id, words):
    response = request_manager_by_text(user_id, words)
    return{
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": "Request forwarded to manager",
        "headers": { }
    }


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
        
        
def send_tool_buttons(user_id):    
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
    
    
def random_event(event, words):
    message_from_slack = dict(urlparse.parse_qsl(event["body"]))
    #print(message_from_slack)
    #payload = loads(event["body"])
    
    #url = "https://slack.com/api/conversations.open"
    url = "https://slack.com/api/chat.postMessage"
    
    # return {
    #     "isBase64Encoded": True,
    #     "statusCode": 200,
    #     "body": dumps("Hi"),
    #     "headers": { }
    # }
    
    #user_info = get_user_info(message_from_slack)
    #print(user_info)
    username = words[1]
    email = words[2]
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    
    data = {
        "channel": "U015QP5QHN0",
        #"channel": message_from_slack["user_id"],
        #"channel": "D014G5CSJ06",
        "text": "Hi, " + message_from_slack["user_name"] + " wants " +  words[0] + " access",
        "attachments": [
            {
                "text": "Choose your action based on the access request",
                "fallback": "Shame... buttons aren't supported in this land",
                "callback_id": "button_tutorial",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "approve",
                        "text": "Approve",
                        "type": "button",
                        "value": words[0],
                        "style": "primary"
                    },
                    {
                        "name": "disapprove",
                        "text": "Disapprove",
                        "type": "button",
                        "value": words[0],
                        "style": "danger"
                    }
                ]
            }
        ]
    }
    
    #print(payload)
    response = requests.request(
        "POST", 
        url,
        headers = headers, 
        data = dumps(data)
    )
    
    json_response = dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    json_response = loads(json_response)
    print(json_response)
    status = json_response["ok"]
    
    if status == True:
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            #"body": dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")),
            "body": "Request sent",
            #"body": dumps(message),
            "headers": { }
        }
    else:
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": "Some error occured",
            "headers":  { }
        }

    
    
    
    