from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_restful import Api
from remote import validate_video, process_video, calculate_spo2, calculate_heart_rate
import shutil
import cv2
import os


app = Flask(__name__)
api = Api(app)

CORS(app)


@app.route('/inference', methods=['POST'])
def inference():
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
                s3_request = body.get("video")
                video_name = s3_request.split('/')[-1]
                os.mkdir('videos/')
                bashCommand = "aws s3 cp " + s3_request + " " + "videos/" + video_name
                os.system(bashCommand)


                file = 'videos/' + video_name
                video = cv2.VideoCapture(file)
                shutil.rmtree('videos')
                validate_video(video)
                video = process_video(video)
                spo2_disc = calculate_spo2(video, discretize=True)
                bpm = calculate_heart_rate(video)

                result = {"name": file.split('/')[-1], "spo2": spo2_disc, 
                        "bpm" : bpm}
                status_code = 200
            else:
                result = {"name": file.split('/')[-1],
                        "message": "Invalid file"}
                status_code = 400
    else:
        result = {'prueba':request.is_json}
        status_code = 400
    return jsonify(result), status_code

@app.route('/health-check', methods=['GET'])
def get():
    return "OK"