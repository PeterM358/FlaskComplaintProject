import boto3
from botocore.exceptions import ClientError
from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:

    def __init__(self):
        self.access_key = config("AWS_ACCESS_KEY")
        self.secret_key = config("AWS_SECRET_KEY")
        self.region = config("AWS_REGION")
        self.bucket = config("AWS_BUCKET_NAME")
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )

    def upload_photo(self, path, key):
        try:
            self.s3.upload_file(path, self.bucket, key)
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        except ClientError as ex:
            raise InternalServerError("S3 is not available at the moment")

    def delete_photo(self, key):
        try:
            resp = self.s3.delete_object(Bucket=self.bucket, Key=key)
            return resp
        except Exception as ex:
            raise Exception(ex)
