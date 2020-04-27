import requests
import os
import json


def getAuthToken():
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    AUDIENCE = os.getenv('AUDIENCE')
    AUTH0_URL = os.getenv('AUTH0_URL')

    try:
        headers = {'content-type': 'application/json'}
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'audience': AUDIENCE,
            'grant_type': 'client_credentials'
        }
        response = requests.post(AUTH0_URL, json.dumps(payload), headers=headers)
        data = response.json()

        return data['access_token']

    except Exception as error:
        print('An error ocurred getting auth token')
        print(error)
