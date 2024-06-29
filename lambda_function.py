import json
import boto3
import pandas as pd
from io import StringIO

# AWS S3 configuration
SOURCE_BUCKET = 'user-logs-2024'
DESTINATION_BUCKET = 'user-data-2024'
SOURCE_KEY = 'user-logs-2024.json'
DESTINATION_KEY = 'user-data-2024.json'

# Initialize S3 client
s3 = boto3.client('s3')

def fetch_data_from_s3(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8')
    if not data:
        raise ValueError("No data found in the S3 object.")
    return data

def save_data_to_s3(data, bucket, key):
    s3.put_object(Bucket=bucket, Key=key, Body=data)

def process_data(data):
    data_io = StringIO(data)
    df = pd.read_json(data_io)
    gender_counts = df['gender'].value_counts()
    gender_counts_dict = gender_counts.to_dict()
    gender_counts_json = json.dumps(gender_counts_dict)
    return gender_counts_json

def lambda_handler(event, context):
    try:
        # Fetch raw data from S3
        data = fetch_data_from_s3(SOURCE_BUCKET, SOURCE_KEY)
        
        # Process the data
        processed_data = process_data(data)
        
        # Save processed data back to S3
        save_data_to_s3(processed_data, DESTINATION_BUCKET, DESTINATION_KEY)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data processed and saved successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
