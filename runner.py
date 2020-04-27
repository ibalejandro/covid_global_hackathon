import json
import os
import traceback
from os import path

import boto3
from botocore.config import Config

from app.services import reports
from remote.estimators import HeartRateEstimator, SpO2Estimator
from remote.readers import NumpyVideo

config_dict = {'connect_timeout': 60000000, 'read_timeout': 6000000}
config = Config(**config_dict)

session = boto3.Session()

s3_client = boto3.client("s3", config=config)
sqs_client = boto3.client('sqs', region_name="us-west-2")

sqs_queue = 'https://sqs.us-west-2.amazonaws.com/240851575709/5vid-processing'


def get_s3_url(record):
    return f"s3://{record['bucket']['name']}/{record['object']['key']}"


def process_video_analysis_requests():
    queue_messages = sqs_client.receive_message(QueueUrl=sqs_queue, MaxNumberOfMessages=10, VisibilityTimeout=60)

    if 'Messages' in queue_messages:
        print(f'Received {len(queue_messages["Messages"])} messages')
        for message in queue_messages['Messages']:
            if 'Body' not in message: continue
            s3_event = json.loads(message['Body'])
            if 'Records' not in s3_event: continue
            records = s3_event['Records']
            for record in records:
                if 's3' not in record:
                    continue
                s3_url = get_s3_url(record['s3'])
                print('Processing url', s3_url)
                result = None

                try:
                    result = process_video_from_url(s3_url)
                    print('Done processing video', s3_url)
                except Exception as error:
                    print('Could not process', s3_url, traceback.print_stack(error))

                if result is not None:
                    try:
                        sqs_client.delete_message(QueueUrl=sqs_queue, ReceiptHandle=message['ReceiptHandle'])
                        print('Deleted sqs message', s3_url)
                    except Exception as error:
                        print('Could not delete message', s3_url, traceback.print_stack(error))

    else:
        print('No messages in queue')


def process_video_from_url(s3_url):
    s3_request = s3_url.replace('s3://', '')
    key = '/'.join(s3_request.split('/')[1:])
    video_name = os.path.basename(key)
    bucket_name = s3_request.split('/')[0]

    if not path.exists('videos/'):
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

    result = {
        "name": s3_url,
        "spo2": spo2,
        "bpm": bpm
    }

    try:
        reports.create_report('ppg', spo2, bpm, s3_url)
    except Exception as e:
        print("Could not create report for", s3_url)
        return None

    return result


process_video_analysis_requests()
