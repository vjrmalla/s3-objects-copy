import boto3
import os
def lambda_handler(event, context):


    DEST_BUCKET='source-lambda-bucket'
    SOURCE_BUCKET='dest-lambda-bucket'
    prefix = ''
    excluded_dir = 's3copy'
    #files = set(os.listdir(local))

    client = boto3.client('s3')
    source_bucket_kwargs = {
    'Bucket':SOURCE_BUCKET,
    'Prefix':prefix,
    }
    dest_bucket_kwargs = {
    'Bucket':DEST_BUCKET,
    'Prefix':prefix,
    }
    #source_bucket = s3.Bucket(SOURCE_BUCKET)
    #dest_bucket = s3.Bucket(DEST_BUCKET)
    source_results = client.list_objects_v2(**source_bucket_kwargs).get('Contents')
    dest_results = client.list_objects_v2(**dest_bucket_kwargs).get('Contents')
    source_objects = [o['Key'] for o in source_results]
    dest_objects = [o['Key'] for o in dest_results]
   # print (source_objects)
    for obj in source_results:
        #print ("I am looking for {} in the destination bucket".format(obj['Key']))
        if not obj['Key'] in dest_objects:
            if not excluded_dir in obj['Key']:
                copy_source = {'Bucket': SOURCE_BUCKET, 'Key': obj['Key']}
                client.copy(copy_source, DEST_BUCKET,obj['Key'])