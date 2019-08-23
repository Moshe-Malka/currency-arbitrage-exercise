import os
import json
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

expected = ['date', 'from_currency', 'to_currency']

def handler(event, context):
    if set(expected) != set(event.keys()):
        message = f"Request Parameters Missing - expected : {expected}. got : {event.keys()}"
        print(message)
        return { 'statusCode' : 401, 'message' : message }
    
    to_currency = event['to_currency']
    from_currency = event['from_currency']

    try:
        objects = s3_client.list_objects_v2(
            Bucket=os.environ['RATES_BUCKET'],
            Prefix=event['date']
            ).get('Contents', [])
    except ClientError as ce:
        print(f"Error While trying to retrive Rates file with Date {event['date']}. Error : {ce}")
        objects = []
    
    # e.g. '2019-08-20/fixed.io/rates.json'
    output = []
    for obj in objects:
        broker_name = obj['Key'].split('/')[1]
        try:
            response = s3_client.get_object(Bucket=os.environ['RATES_BUCKET'], Key=obj['Key'])
            file_content = response['Body'].read().decode('utf-8') 
            json_content = json.loads(file_content)
        except ClientError as ce:
            json_content = {}
            print("Error When trying to retrive file content from S3.")

        _to = json_content.get(to_currency, None)
        _from = json_content.get(from_currency, None)
        if _to == None or _from == None:
            rate = None
        else:
            rate =  _to / _from
        output.append({ 'broker' : broker_name, 'rate' : str(rate) })

    return output