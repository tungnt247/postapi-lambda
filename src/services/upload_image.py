import os
import boto3

s3 = boto3.client('s3',
                    region_name=os.getenv('REGION'),
                    aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))

class UploadImageService:
    def upload(self, post_id, image):
        if image.filename == '':
            return None

        try:
            key = f'{post_id}/{image.filename}'
            bucket = os.getenv('S3_BUCKET')
            s3.put_object(
                Body=image,
                Bucket=bucket,
                Key=key,
                ContentType=image.mimetype
            )
            return f'https://{bucket}.s3-ap-southeast-1.amazonaws.com/{key}'
        except Exception as e:
            print(e)
