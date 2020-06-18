import logging
import boto3
from botocore.exceptions import ClientError
import os
import json

creds_file = os.path.abspath(os.path.join('..', "credentials/credentials_aws.json"))

with open(creds_file, "r") as f:
    json_data = json.loads(f.read())

ACCESS_KEY = json_data["AWSAccessKeyId"]
SECRET_KEY = json_data["AWSSecretKey"]
# SESSION_TOKEN = json_data["AWSSessionToken"]

def oauth_login():

    client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    return client

def get_bucket_list(client):
    """Retrieve the list of existing buckets

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        response = client.list_buckets()

        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'    {bucket["Name"]}')

    except Exception as e:
        logging.error(e)
        print(f"An error has occurred {e}")


def create_bucket(client, bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param
        bucket_name: Bucket to create
        region: String region to create bucket in, e.g., 'ap-south-1' for AWS mumbai
    :return: True if bucket created, else False
    """

    try:
        if region is None:
            client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    except ClientError as e:
        print(f"An error has occurred {e}")
        return False
    return True


def delete_bucket(client, bucket_name):
    """Delete an S3 bucket
    :param
        bucket_name: Bucket to create
    :return: True if bucket created, else False
    """

    try:
        client.delete_bucket(Bucket=bucket_name)

    except ClientError as e:
        print(f"An error has occurred {e}")
        return False
    return True


def get_bucket_permissions(client, bucket_name):
    """S3 bucket permissions
    :param
        bucket_name: Bucket to create
    :return: permissions list of the bucket
    """

    try:
        result = client.get_bucket_acl(
            Bucket=bucket_name
        )
        print(result["Grants"][0]["Permission"])
        return result

    except ClientError as e:
        print(f"An error has occurred {e}")
        return None


def modify_bucket_permissions(client, bucket_name, permission):
    """Modify S3 bucket permissions
    :param
        bucket_name: Bucket to create
        client: s3 session
    :return: permissions list of the bucket
    """

    try:
        response = client.put_bucket_acl(AccessControlPolicy={'Grants': [{'Permission': permission}]}, Bucket=bucket_name)
        print(response)

    except ClientError as e:
        print(f"An error has occurred {e}")
        return None


def get_file_permissions(client, bucket_name, file_name):
    """S3 file permissions
    :param
        bucket_name: Bucket in which the file is present
        file_name: File name for which the metadata is required
    :return: permissions list of the file
    """

    try:
        result = client.get_object_acl(
            Bucket=bucket_name,
            Key=file_name
        )
        print(result["Grants"])
        return result

    except ClientError as e:
        print(f"An error has occurred {e}")
        return None


def modify_file_permissions(client, bucket_name, file_name, permission):
    """Modify S3 bucket permissions
    :param
        bucket_name: Bucket to create
        client: s3 session
    :return: permissions list of the bucket
    """

    try:
        response = client.put_object_acl(AccessControlPolicy={'Grants': [{'Permission': permission}]}, Bucket=bucket_name, Key=file_name)
        print(response)

    except ClientError as e:
        print(f"An error has occurred {e}")
        return None


def get_file_details(client, bucket_name, file_name):
    """S3 file permissions
    :param
        bucket_name: Bucket in which the file is present
        file_name: File name for which the metadata is required
    :return: permissions list of the file
    """

    try:
        result = client.get_object(
            Bucket=bucket_name,
            Key=file_name
        )
        print(result)
        # print(vars(result["Body"]._raw_stream._original_response.msg))
        return result

    except ClientError as e:
        print(f"An error has occurred {e}")
        return None


def upload_file(client, file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param
        file_name: File to upload
        bucket: Bucket to upload to
        object_name: S3 object name. If not specified then file_name is used
    :returns
        True if file was uploaded, else False
    """

    if object_name is None:
        object_name = file_name

    try:
        response = client.upload_file(file_name, bucket, object_name)

    except Exception as e:
        print(f"An error has occurred: {e}")
        # logging.error(e)
        return False
    return True


def download_file(client, file_name, bucket, object_name=None):
    """Download a file from an S3 bucket

    :param
        client: s3 session
        file_name: File to be saved as
        object_name: File to be downloaded
        bucket: Bucket from which the file has to be downloaded
    :returns
        True if file was uploaded, else False
    """
    if object_name is None:
        object_name = file_name

    try:
        with open(file_name, 'wb') as f:
            client.download_fileobj(bucket, object_name, f)

    except Exception as e:
        print(f"An error has occurred: {e}")
        # logging.error(e)
        return False
    return True


def delete_file(client, file_name, bucket):
    """Upload a file to an S3 bucket

    :param
        file_name: File to upload
        bucket: Bucket to upload to
        object_name: S3 object name. If not specified then file_name is used
    :returns
        True if file was uploaded, else False
    """

    try:
        client.delete_object(Bucket=bucket, Key=file_name)

    except Exception as e:
        print(f"An error has occurred: {e}")
        # logging.error(e)
        return False
    return True


