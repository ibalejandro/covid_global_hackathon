import requests
import json
from app.services.auth import getAuthToken


def create_report(telemetry_type, spo2_disc, bpm, s3_url):
    try:
        token = getAuthToken()
        headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
        reports_url = 'https://reports-api-dev.5vid.co/api/v1/telemetry-reports/'
        payload = {
            "telemetry_type": telemetry_type,
            "telemetry_report": {
                "spo2": spo2_disc,
                "bpm": bpm
            },
            "telemetry_source_id": s3_url
        }

        response = requests.post(reports_url, json.dumps(payload), headers=headers)
        data = response.json()
        print(data)

        return response.json()

    except Exception as error:
        print('An error ocurred getting auth token')
        print(error)
