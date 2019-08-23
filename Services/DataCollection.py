import os
import json
import requests
import boto3
from botocore.exceptions import ClientError
from datetime import date, timedelta
import re

pat = re.compile(r'\d{4}\-\d{2}\-\d{2}')

s3_client = boto3.client('s3')

def handler(event, context):
    if 'date' in event.keys():  # Manual initiation
        if pat.match(event['date']):    # e.g. 2019-08-23
            date_param = event['date']
        else:
            print(f"'date' param does not match to expected format. got {event['date']} expexted YYYY-MM-DD")
            return { "statusCode" : 401, "message" : f"'date' param does not match to expected format. got {event['date']} expexted YYYY-MM-DD" }
    else:
        yesterday = date.today() - timedelta(days=1)    # Scheduled
        date_param = yesterday.strftime('%Y-%m-%d')

    # read json file from S3 with brokers data.
    try:
        brokers_file = s3_client.get_object(
            Bucket=os.environ['BROKERS_BUCKET'],
            Key=os.environ['BROKERS_FILENAME']
            )
        brokers_content = brokers_file['Body'].read().decode('utf-8')
        brokers = json.loads(brokers_content)['brokers']
    except ClientError as ce:
        print(ce)
        return { "statusCode" : 500, "message" : "Error While trying to retrive brokers file.", "error" : str(ce) }
    
    # for each broker - issue a get request and store response in S3.
    # NOTE: this is assumming there are not a lot of brokers,
    # as this can make the lambda timeout (current operation is ~500 ms per broker request).
    # other option is using a combination of lambdas and sns and or sqs.

    for broker in brokers:
        print(f"Getting rates from broker {broker['broker']}")
        if 'api_key' in broker.keys():
            req_uri = f"{broker['base']}/{date_param}?{broker['api_key']}&base=USD"
        else:
            req_uri = f"{broker['base']}/{date_param}?base=USD"
        try:
            print(f"Requesting {req_uri} ...")
            broker_response = requests.get(req_uri)
        except Exception as e:
            print(f"Error while trying to request broker {broker['broker']} - {e}.")
        if broker_response.status_code == 200:
            print(broker_response.text)
            data = broker_response.text
            if 'success' in json.loads(data) and not json.loads(data)['success']:
                print("Request to broker failed!")
            else:
                if 'rates' in json.loads(data).keys():
                    data = json.dumps(json.loads(data)['rates'])
                try:
                    s3_response = s3_client.put_object(
                        Body=data,
                        Bucket=os.environ['RATES_BUCKET'],
                        Key=f"{date_param}/{broker['broker']}/rates.json"
                        )
                except ClientError as ce:
                    print(f"Error While trying to retrive brokers file - {ce}")
        else:
            print(f"Request to broker {broker['broker']} failed! - {broker_response.content} - {req_uri}")