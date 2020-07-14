import requests
import json
import time
from datetime import datetime
import subprocess
import boto3


import wasabiconfig as cfg


endpoint = cfg.s3["endpoint_url"]
aws_access_key = cfg.s3["aws_access_key_id"]
aws_secret_key = cfg.s3["aws_secret_access_key"]
wasabi_bucket = cfg.s3["wasabi_bucket"]

s4 = boto3.client('s3',
endpoint_url = endpoint,
aws_access_key_id = aws_access_key,
aws_secret_access_key = aws_secret_key)

# todays\'s epoch
tday = time.time()
duration = 86400*3 #3 days in epoch seconds
#checkpoint for deletion
expire_limit = tday - duration
# initialize s3 client
file_size = [] #just to keep track of the total savings in storage size


#works to only get us key/file information
def get_key_info(bucket):

    key_names = []
    file_timestamp = []
    file_size = []
    kwargs = {"Bucket": bucket}
    while True:
        response = s4.list_objects_v2(**kwargs)
        for obj in response["Contents"]:
            # exclude directories/folder from results. Remove this if folders are to be removed too
            if "." in obj["Key"]:
                key_names.append(obj["Key"])
                file_timestamp.append(obj["LastModified"].timestamp())
                file_size.append(obj["Size"])
        try:
            kwargs["ContinuationToken"] = response["NextContinuationToken"]
        except KeyError:
            break

    key_info = {
        "key_path": key_names,
        "timestamp": file_timestamp,
        "size": file_size
    }
    return key_info

# connect to s3 and delete the file
def delete_s3_file(file_path, bucket):
    print(f"Deleting {file_path}")
    s4.delete_object(Bucket=bucket, Key=file_path)
    return True

# Check expiration date
def check_expiration(key_date=tday, limit=expire_limit):
    if key_date < limit:
        return True



def delete_files(bucket):
    s3_file = get_key_info(bucket)
    # i is the counter 
    for i, fs in enumerate(s3_file["timestamp"]):
        print(i, fs)
        file_expired = check_expiration(fs)
        if file_expired: #if True is recieved
            delete_s3_file(s3_file["key_path"][i], bucket)
 

delete_files("waxtest2")


