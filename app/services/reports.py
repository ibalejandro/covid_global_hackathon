import os

import requests
import json
from app.services.auth import getAuthToken


def create_report(telemetry_type, spo2_disc, bpm, valid_spo2, valid_bpm, s3_url):
        token = getAuthToken()
        headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
        reports_url = os.getenv('REPORTS_API_URL')
        payload = {
            "telemetry_type": telemetry_type,
            "telemetry_report": {
                "spo2": spo2_disc,
                "bpm": bpm,
                "bpmValid": bool(valid_bpm),
                "spo2Valid": bool(valid_spo2)
            },
            "telemetry_source_id": s3_url
        }

        print(payload)

        response = requests.post(reports_url, json.dumps(payload), headers=headers)

        return response.json()
