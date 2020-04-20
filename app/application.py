from flask import Flask, render_template, request, jsonify
import boto3
from botocore.config import Config
from flask_cors import CORS
from remote.readers import NumpyVideo
from remote.estimators import HeartRateEstimator, SpO2Estimator
import shutil
import cv2
import os
import sys
import traceback


application = Flask(__name__)

CORS(application)

config_dict = {'connect_timeout': 60000000, 'read_timeout': 6000000}
config = Config(**config_dict)
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=config
)



@application.route('/inference', methods=['POST'])
def inference():
    try:
        if request.is_json:
                is_body_well_formed = True
                try:
                    body = request.json
                except:
                    is_body_well_formed = False
                    result = {
                        "message": "Specify a well-formed body"
                    }
                    status_code = 400
                if is_body_well_formed:
                    s3_request = body.get("video").replace('s3://', '')
                    key = '/'.join(s3_request.split('/')[1:])
                    video_name = os.path.basename(key)
                    bucket_name = s3_request.split('/')[0]
                    os.mkdir('videos/')
                    file = 'videos/' + video_name
                    s3_client.download_file(bucket_name, key, file)

                    video = NumpyVideo(file)
                    spo2, is_valid_spo2 = SpO2Estimator().estimate(video)
                    bpm, is_valid_bpm = HeartRateEstimator().estimate(video)

                    if not is_valid_spo2:
                        spo2 = None

                    if not is_valid_bpm:
                        bpm = None

                    result = {"name": file.split('/')[-1], "spo2": spo2,
                            "bpm" : bpm}
                    status_code = 200
                else:
                    result = {"name": file.split('/')[-1],
                            "message": "Invalid file"}
                    status_code = 400
        else:
            result = {'prueba':request.is_json}
            status_code = 400
    except Exception as e:

        print('***** Error processing video *******')
        print(traceback.format_exc())
        print(' **** error **** ')
        print(e)

    finally:
        shutil.rmtree('videos')

    return jsonify(result), status_code

@application.route('/health-check', methods=['GET'])
def get():
    return "OK"