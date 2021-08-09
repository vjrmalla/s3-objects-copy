import boto3
import os
import logging
import botocore

logger = logging.getLogger()
logger.setLevel(os.getenv('debug_level', 'INFO'))

DEST_BUCKET = os.environ.get('DST_BUCKET')
SOURCE_BUCKET = os.environ.get('SRC_BUCKET')
REGION = os.environ.get('REGION')
client = boto3.client('s3')
def handler(event, context):
    main(event, logger)

def main(event, logger):
    try:
        prefix = ''
        excluded_dir = 's3copy'
        #files = set(os.listdir(local))
        source_bucket_kwargs = {
        'Bucket':SOURCE_BUCKET,
        'Prefix':prefix,
        }
        dest_bucket_kwargs = {
        'Bucket':DEST_BUCKET,
        'Prefix':prefix,
        }
        source_results = client.list_objects_v2(**source_bucket_kwargs).get('Contents')
        dest_results = client.list_objects_v2(**dest_bucket_kwargs).get('Contents')
        source_objects = [o['Key'] for o in source_results]
        if (dest_results):
            dest_objects = [o['ETag'] for o in dest_results]
        #dest_objects = [o['Key'] for o in dest_results]
        # print (source_objects)
        index = 0
        for obj in source_results:
            index += 1
            #print ("I am looking for {} in the destination bucket".format(obj['Key']))
            if (dest_results):
                if not obj['ETag'] in dest_objects:
                    if not excluded_dir in obj['Key']:
                        copy_objects(SOURCE_BUCKET, DEST_BUCKET, obj['Key'], logger)
            else:
                if not excluded_dir in obj['Key']:
                    copy_objects(SOURCE_BUCKET, DEST_BUCKET, obj['Key'], logger)
        logger.info('number of objects copied:'+ index)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "AccessDenied":
            print("Error: Access denied!!")
        elif e.response['Error']['Code'] == "InvalidBucketName":
            print("Error: Invalid bucket name!!")
        elif e.response['Error']['Code'] == "NoSuchBucket":
            print("Error: No such bucket!!")
        else:
            raise

def copy_objects(srcbucket, destbucket, key, logger):
    copy_source = {'Bucket': srcbucket, 'Key': key}
    client.copy(copy_source, destbucket, key)
    
