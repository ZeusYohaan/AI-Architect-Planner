import boto3
import configparser
import os
from botocore.exceptions import ClientError

config = configparser.ConfigParser()
config.read('config.ini')


def connect_to_s3():
    s3 = boto3.resource(
        "s3",
        region_name='us-east-1',
        aws_access_key_id=config["s3 bucket connection"]["AWS_KEY_ID"],
        aws_secret_access_key=config["s3 bucket connection"]["AWS_SECRET"]
    )
    bucket = s3.Bucket(config["s3 bucket connection"]["Bucket_name"])
    return bucket

def save_file(args, filepath):
    bucket = connect_to_s3()
    user_id = args['user_id']
    file_des = args['file_des']

    try:
        full_path = filepath
        s3_key = f"{user_id}/{file_des}/{filepath}"
        print(full_path)
        print(s3_key)
        with open(full_path, 'rb') as data:
            bucket.put_object(Key=s3_key, Body=data)
            return s3_key,None
    except Exception as e:
        print(e)
        return None,e