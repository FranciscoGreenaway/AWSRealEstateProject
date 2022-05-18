import boto3
import json

def put_object_S3(data_buffer, file_name):

    bucket = 'real-estate-extracted-data'

    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, file_name).put(Body=data_buffer.getvalue())
