import boto3

def upload_to_s3():
    """Upload a file to my S3 bucket"""

    # these 3 things need to be hidden for public use
    REGION = 'your bucket region' #eg 'us-east-1'
    ACCESS_KEY_ID= 'your access key' #eg 'BPLDERWBSPFCARQ7GLAP'
    SECRET_ACCESS_KEY= 'your secret access key' #keep hidden!!!

    PATH_IN_COMPUTER = 'file path' # name of the local file being uploaded
    BUCKET_NAME = 'your bucket name' # eg 'my-bucket'
    KEY = 'file' # name of the file where your upload will be stored in your bucket


    s3_resource = boto3.resource(
        's3',
        region_name = REGION,
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
    )
    s3_resource.Bucket(BUCKET_NAME).put_object(
        Key = KEY,
        # below opens the local file in binary to be uploaded (important!)
        Body = open(PATH_IN_COMPUTER, 'rb')
    )
    return

upload_to_s3()
