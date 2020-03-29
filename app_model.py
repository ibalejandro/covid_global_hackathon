from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from remote import validate_video, process_video, calculate_spo2, calculate_heart_rate, discretize_spo2

import cv2
import os


app = Flask(__name__)

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
                os.rmdir(file)
                validate_video(video)
                video = process_video(video)
                spo2 = calculate_spo2(video)
                spo2_disc = calculate_spo2(video, discretize=True)
                bpm = calculate_heart_rate(video)
                bpm_disc = calculate_heart_rate(video, discretize=False)

                result = {"name": file.split('/')[-1], "spo2": spo2, 
                          "spo2_disc": spo2_disc, "bpm" : bpm, "bpm_disc": bpm_disc}

                status_code = 200
            else:
                result = {"name": file.split('/')[-1],
                        "message": "Invalid file"}
                status_code = 400
    else:
        result = {'prueba':request.is_json}
        status_code = 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
