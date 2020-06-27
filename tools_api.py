from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth
from helper_functions import get_user_info

access_token = "XXXXXXXXXXXXXX"
verification_token = "XXXXXXXXXXXXXX"

# to get github access
def github_handler(username, user_id):
    git_token = "XXXXXXXXXXXXXX"
    

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
    
    #print(dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")),
        "headers": { }
    }
    
    
# to get jira access    
def jira_handler(user_id):
    jira_token = "XXXXXXXXXXXXXX"
    user_info = get_user_info(user_id)
    user_profile = user_info["profile"]
    username = user_profile["display_name"]
    email = user_profile["email"]
    #print(username," : ", email)
    
    url = "https://sunilbansiwal.atlassian.net/rest/api/3/user"

    auth = HTTPBasicAuth("sunilssb786@gmail.com", jira_token)
    
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    
    payload = dumps( {
      "emailAddress": email,
      "displayName": username,
    })
    
    response = requests.request(
      "POST",
      url,
      data=payload,
      headers=headers,
      auth=auth
    )
    
    print(dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")),
        "headers": { }
    }

