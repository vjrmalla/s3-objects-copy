import boto3
import os
import logging
import botocore
from botocore.client import Config

logger = logging.getLogger()
logger.setLevel(os.getenv('debug_level', 'INFO'))

config = Config(connect_timeout=5, retries={'max_attempts': 0})
client = boto3.client('s3', config=config)

#client = boto3.client('s3')
def handler(event, context):
    main(event, logger)

def main(event, logger):
    try:
        DEST_BUCKET = os.environ.get('DST_BUCKET')
        SOURCE_BUCKET = os.environ.get('SRC_BUCKET')
        REGION = os.environ.get('REGION')
        prefix = ''
        # Create a reusable Paginator
        paginator = client.get_paginator('list_objects_v2')
        print ('after paginator')

        # Create a PageIterator from the Paginator
        page_iterator_src = paginator.paginate(Bucket=SOURCE_BUCKET,Prefix = prefix)
        page_iterator_dest = paginator.paginate(Bucket=DEST_BUCKET,Prefix = prefix)
        print ('after page iterator')
        index = 0
        for page_source in page_iterator_src:
            for obj_src in page_source['Contents']:
                flag = "FALSE"
                for page_dest in page_iterator_dest:
                    for obj_dest in page_dest['Contents']:
                        # checks if source ETag already exists in destination
                        if obj_src['ETag'] in obj_dest['ETag']:
                            flag = "TRUE"
                            break
                    if flag == "TRUE":
                        break
                if flag != "TRUE":
                    index += 1
                    client.copy_object(Bucket=DEST_BUCKET, CopySource={'Bucket': SOURCE_BUCKET, 'Key': obj_src['Key']}, Key=obj_src['Key'],)
                    print ("source ETag {} and destination ETag {}".format(obj_src['ETag'],obj_dest['ETag']))
                    print ("source Key {} and destination Key {}".format(obj_src['Key'],obj_dest['Key']))
        print ("Number of objects copied{}".format(index))
        logger.info("number of objects copied {}:".format(index))
    except botocore.exceptions.ClientError as e:
        raise
