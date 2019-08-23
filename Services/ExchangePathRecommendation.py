import os, math, json
import boto3
from botocore.exceptions import ClientError
import re

pat = re.compile(r'\d{4}\-\d{2}\-\d{2}')

s3_client = boto3.client('s3')

def handler(event, context):
    if 'date' not in event.keys() or not pat.match(event['date']): # e.g. 2019-08-23
        print("Missing / Wrong 'date' param in request.")
        return { "statusCode" : 401, "message" : "Missing / Wrong 'date' param in request." }
    try:
        objects = s3_client.list_objects_v2(
            Bucket=os.environ['RATES_BUCKET'],
            Prefix=event['date']
            )['Contents']
    except ClientError as ce:
        print(f"Error While trying to retrive Rates file with Date {event['date']}- {ce}")
        objects = []
    
    output = []
    for obj in objects:
        broker_name = obj['key'].split('/')[1]
        try:
            response = s3_client.get_object(Bucket=os.environ['RATES_BUCKET'], Key=obj['key'])
            file_content = response['Body'].read().decode('utf-8') 
            json_content = json.loads(file_content)
        except ClientError as ce:
            json_content = {}
            print("Error When trying to retrive file content from S3.")

        # TODO: find optimal path on directed graph.
        
        # add to output array
        output.append({
            'broker' : broker_name,
            'from' : '',
            'to' : '',
            'rate' : ''
            })

    return output