import boto3
import sys
import os
import logging

from pathlib import Path
from botocore.exceptions import ClientError
from botocore.client import Config

# logging.basicConfig(level=logging.INFO)


def upload(s3, f, bucket, object_name=None):
    # from https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    if object_name is None:
        object_name = os.path.basename(f)

    try:
        response = s3.meta.client.upload_file(f, bucket, object_name)
        logging.info(f"{f} uploaded.")
    except ClientError as e:
        logging.error(e)
        return


def needs_update(obj, f):
    # from https://stackoverflow.com/questions/44532078/how-to-check-if-local-file-is-same-as-s3-object-without-downloading-it-with-boto
    logging.info(int(obj.last_modified.strftime('%s')))
    logging.info(int(os.path.getmtime(f)))
    return int(obj.last_modified.strftime('%s')) + 2000 < int(os.path.getmtime(f))


def sync(dir_name, bucket_name, s3):

    if bucket_name not in [bucket.name for bucket in s3.buckets.all()]:
        print("Remote bucket does not exist. Creating bucket...")
        try:
            s3.create_bucket(Bucket=bucket_name)  # handle name correctness?
        except ClientError as e:
            logging.error(e)
            print("ClientError: could not create the bucket.")
            return

    remote_bucket = s3.Bucket(bucket_name)

    root_dir = Path(dir_name)
    files = [str(f) for f in root_dir.glob('**/*') if f.is_file()]

    for f in files:
        obj_name = f

        if obj_name not in [obj.key for obj in remote_bucket.objects.all()]:
            upload(s3, obj_name, bucket_name, object_name=obj_name)
        else:
            if needs_update(s3.Object(bucket_name, obj_name), obj_name):
                upload(s3, obj_name, bucket_name, object_name=obj_name)

    for obj in remote_bucket.objects.all():
        if obj.key not in files:
            obj.delete()
            logging.info("Object deleted.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python main.py LOCAL_DIR REMOTE_BUCKET")
    else:
        local_dir = sys.argv[1]
        remote_bucket_name = sys.argv[2]

        s3 = boto3.resource('s3',
                            endpoint_url="http://172.17.0.2:9000",
                            aws_access_key_id="minio",
                            aws_secret_access_key="miniokey",
                            config=Config(signature_version="s3v4"))

        sync(local_dir, remote_bucket_name, s3)
