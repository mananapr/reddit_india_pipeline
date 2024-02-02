import sys
import boto3
import pathlib
from dotenv import dotenv_values

## Read env file
script_path = pathlib.Path(__file__).parent.resolve()
config = dotenv_values(f"{script_path}/configuration.env")
AWS_BUCKET = config["bucket_name"]
ACCESS_KEY_ID = config['aws_access_key_id']
SECRET_ACCESS_KEY = config['aws_secret_access_key']

## Bronze or Silver
data_level = sys.argv[1]
filename = f"{data_level}.csv"

if __name__ == "__main__":
    s3_conn = boto3.resource("s3", aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    s3_conn.meta.client.upload_file(Filename=f"/tmp/{filename}", Bucket=AWS_BUCKET, Key=filename)
