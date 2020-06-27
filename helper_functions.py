from json import loads, dumps
from botocore.vendored import requests
import boto3
import sys
import base64
import os
from urllib import parse as urlparse
from botocore.vendored.requests.auth import HTTPBasicAuth

access_token = "XXXXXXXXXXXXXXXXXXX"
verification_token = "XXXXXXXXXXXXXXXXXXX"

# To get user info from the user_id 
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
        

