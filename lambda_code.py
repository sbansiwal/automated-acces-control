from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth

access_token = 'xoxb-1133836710359-1171538815537-ZTSZL4B92kh0UGAaowWR0l5C'
verification_token = 'PxKCVNMUEznFN5BPhthV4ETf'

# def lambda_handler(event, context):
#     message_from_slack = dict(urlparse.parse_qsl(event["body"]))
    
#     jiraID = message_from_slack['text']
    
#     url = "https://sunilbansiwal.atlassian.net/rest/api/3/issue/" + str(jiraID)
    
#     auth = HTTPBasicAuth("sunilssb786@gmail.com", "ZDKt2Uch4SqwbzXQAQRn78F4")

#     headers = {
#       "Accept": "application/json"
#     }
    
#     response = requests.request(
#       "GET",
#       url,
#       headers=headers,
#       auth=auth
#     )
    
#     print(dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    
#     issue_payload = loads(response.text)
    
#     val = "false"
    
#     if "errorMessages" in issue_payload:
#         val = "true"

#     if val == "false":
#         return {
#             "isBase64Encoded": True,
#             'statusCode': 200,
#             'body': "Issue status: " + issue_payload['fields']['status']['name'],
#             'headers': { }
#         }
#     else:
#         return {
#             "isBase64Encoded": True,
#             'statusCode': 200,
#             'body':issue_payload["errorMessages"][0],
#             'headers': { }
#         }

def lambda_handler(event, context):
    message_from_slack = dict(urlparse.parse_qsl(event["body"]))
    #print(message_from_slack)
    username = message_from_slack["text"]
    #print(text)
    
    # print(username)
    # print(email)
    
    # return {
    #     "isBase64Encoded": True,
    #     "statusCode": 200,
    #     "body": username,
    #     "headers": { }
    # }
    
    url = "https://api.github.com/orgs/test-webhook-events/memberships/" + str(username)
    
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorisation": "token " + git_token
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
    
# def lambda_handler(event, context):
#     message_from_slack = dict(urlparse.parse_qsl(event["body"]))
#     #print(message_from_slack)
#     text = message_from_slack["text"]
#     #print(text)
    
#     username, email = text.split(' ', 1)
    
#     # print(username)
#     # print(email)
    
#     # return {
#     #     "isBase64Encoded": True,
#     #     "statusCode": 200,
#     #     "body": username,
#     #     "headers": { }
#     # }
    
#     url = "https://sunilbansiwal.atlassian.net/rest/api/3/user"

#     auth = HTTPBasicAuth("sunilssb786@gmail.com", jira_token)
    
#     headers = {
#       "Accept": "application/json",
#       "Content-Type": "application/json"
#     }
    
#     payload = dumps( {
#       "emailAddress": email,
#       "displayName": username,
#     })
    
#     response = requests.request(
#       "POST",
#       url,
#       data=payload,
#       headers=headers,
#       auth=auth
#     )
    
#     print(dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

#     return {
#         "isBase64Encoded": True,
#         "statusCode": 200,
#         "body": dumps(loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")),
#         "headers": { }
#     }
    
