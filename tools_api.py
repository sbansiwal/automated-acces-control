from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
from helper_functions import get_user_info

from google.cloud import bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build

# READ THESE FROM .ENV FILE
DELEGATED_EMAIL = "dispatch.test@razorpay.com"
SERVICE_ACCOUNT_FILE = "cred.json"

# to get github access
def github_handler(username, user_id):
    git_token = "XXXXXXXXXXXXXXXXXXX"
    url = "https://api.github.com/orgs/test-webhookevents/memberships/" + str(username)
    #url = "https://api.github.com/orgs/test-webhook-events/members"

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "Bearer " + git_token
    }
    
    payload = dumps( {
      "role": "member"
    })
    
    response = requests.request(
      "PUT",
      url,
      data=payload,
      headers=headers
    )
    
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")),
        "headers": { }
    }
   
# to get jira access    
def jira_handler(user_id):
    jira_token = "XXXXXXXXXXXXXXXXXXX"
    user_info = get_user_info(user_id)
    user_profile = user_info["profile"]
    username = user_profile["display_name"]
    email = user_profile["email"]
    
    url = "https://sunilbansiwal.atlassian.net/rest/api/3/user"

    auth = HTTPBasicAuth("sunilssb786@gmail.com", jira_token)
    
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    
    payload = dumps( {
      "emailAddress": "testsunilbansiwal@gmail.com",
      "displayName": username,
    })
    
    response = requests.request(
      "POST",
      url,
      data=payload,
      headers=headers,
      auth=auth
    )
    
    print("Jira reponse : ", response.text)
 
    reponse = dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    json_response = loads(reponse)
    return json_response

# RETURNS SERVICE OBJECT TO CLIENT FOR GOOGLE APIS
def getService():
    # CURRENT AUTH, THIS AUTH CAN BE USED FOR ALL GROUP OPERATIONS
    scopes = ["https://www.googleapis.com/auth/admin.directory.group", ]
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes, )
    credss = creds.with_subject(DELEGATED_EMAIL)
    service = build('admin', 'directory_v1', credentials=credss, )
    return service

def add_member(group_key, email):
    try:
        service = getService()
        response = service.members().insert(groupKey=group_key, body={'email': email}, ).execute()
        return response
    except Exception as error:
        if error.resp.status in [409]:
            return '', 200
        return error

# WILL NEED TO UPDATE THIS IF FURTHER INFO PROVIDED
def getAccess(toolName, email):
    if(toolName == "Vajra"):
        return add_member("backend@razorpay.com",email)
    elif(toolName == "Deployment"):
        return add_member("tech.leads@razorpay.com",email)
    else:
        return add_member("developers@razorpay.com",email)

    

