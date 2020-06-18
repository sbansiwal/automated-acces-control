from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth

<<<<<<< HEAD
#access_token = "xoxb-1133836710359-1171538815537-ZTSZL4B92kh0UGAaowWR0l5C"
access_token = "xoxb-XXXXXXXXXX-XXXXXXXXXXX-XXXXXXXXXXXXXX"
verification_token = "XXXXXXXXXXXXXXXX"
=======
access_token = "XXX-YYYYYYYYYY-XXXXXXX-YYYYYYYYYY'
verification_token = "XXXXXXXXXXXXX"
git_token = "YYYYYYYYYYYYY"
jira_token = "XXXXXXXXXXXX"
>>>>>>> e312db4d229cae977e70ef8522245d7d2454fad5

def lambda_handler(event, context):
    
    slack_payload = dict(urlparse.parse_qsl(event["body"]))
    slack_message = slack_payload["text"]
    words = slack_message.split(' ')
    
    if words[0] == "Jira":
        return jira_handler(words)
    elif words[0] == "Github":
        return github_handler(words)
    else:
        return random_event(event, context)


# FOR GITHUB
def github_handler(slack_message):
    git_token = "XXXXXXXXXXXXXXXXXXX"
    
    username = slack_message[1]
    print(username)

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
    
    print(dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")),
        "headers": { }
    }
    
    
# FOR JIRA CLOUD    
def jira_handler(slack_message):
    jira_token = "XXXXXXXXXXXXXXXXXXX"
    username = slack_message[1]
    email = slack_message[2]
    
    # print(username)
    # print(email)
    
    # return {
    #     "isBase64Encoded": True,
    #     "statusCode": 200,
    #     "body": username,
    #     "headers": { }
    # }
    
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


def random_event(event, context):
    message_from_slack = dict(urlparse.parse_qsl(event["body"]))
    #payload = loads(event["body"])
    
    url = "https://slack.com/api/conversations.open"
    
    # return {
    #     "isBase64Encoded": True,
    #     "statusCode": 200,
    #     "body": dumps("Hi"),
    #     "headers": { }
    # }
    
    headers = {
        "Content-type": "application/json", 
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token,
    }
    
    data = {
        "users": "U015QP5QHN0",
        "text": "Hi",
        "charset": "test"
    }
    
    #print(payload)
    response = requests.request(
        "POST", 
        url,
        headers = headers, 
        data = dumps(data)
    )
    
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "body": dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")),
        "headers": { }
    }

<<<<<<< HEAD
    
    
    
    
=======
#     return {
#         "isBase64Encoded": True,
#         "statusCode": 200,
#         "body": dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")),
#         "headers": { }
#     }
    
>>>>>>> e312db4d229cae977e70ef8522245d7d2454fad5
