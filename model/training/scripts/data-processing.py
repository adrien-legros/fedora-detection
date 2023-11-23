import tarfile
import os
import subprocess


def init_s3_connection():
    import boto3
    key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    endpoint = os.environ.get("AWS_S3_ENDPOINT")
    s3_client = boto3.client("s3", aws_access_key_id=key_id, aws_secret_access_key=secret_key, endpoint_url=endpoint)
    return s3_client

        
if __name__ == "__main__":
    req = "pip install -r requirements.txt"
    subprocess.run(req.split())
    bucket_name = os.environ.get("AWS_S3_BUCKET")
    s3_client = init_s3_connection()
    # os.makedirs("../data", exist_ok = True)
    s3_client.download_file(bucket_name, "data/dataset.tar.gz", "/opt/app-root/src/data/dataset.tar.gz")
    tar = tarfile.open("/opt/app-root/src/data/dataset.tar.gz")
    tar.extractall(path="/opt/app-root/src/data")
    tar.close()