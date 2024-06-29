import boto3
import pandas as pd
from io import StringIO
import json

# AWS S3 credentials and bucket names
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
SOURCE_BUCKET = 'user-logs-2024'
DESTINATION_BUCKET = 'user-data-2024'
SOURCE_KEY = 'user-logs-2024.json'
DESTINATION_KEY = 'user-data-2024.json'

# Initialize boto3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

# Fetch JSON data from S3
def fetch_data_from_s3(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read().decode('utf-8')
    print("1 - Data fetched from the source S3 bucket")
    if not data:
        raise ValueError("No data found in the S3 object.")
    return data

# Save data to S3
def save_data_to_s3(data, bucket, key):
    s3.put_object(Bucket=bucket, Key=key, Body=data)

# Process the data
def process_data(data):
    data_io = StringIO(data)
    db = pd.read_json(data_io)
    gender_counts = db['gender'].value_counts()
    gender_counts_dict = gender_counts.to_dict()
    gender_counts_json = json.dumps(gender_counts_dict)
    print("2 - Data Processed with Pandas")
    print(gender_counts_json)
    return  (gender_counts_json)

# Main function
data = fetch_data_from_s3(SOURCE_BUCKET, SOURCE_KEY)   
processed_data = process_data(data)
save_data_to_s3(processed_data, DESTINATION_BUCKET, DESTINATION_KEY)
print("3 - Data data saved to the destination s3 Bucket")
