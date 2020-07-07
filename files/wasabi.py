import boto3 
import wasabiconfig as cfg


endpoint = cfg.s3["endpoint_url"]
aws_access_key = cfg.s3["aws_access_key_id"]
aws_secret_key = cfg.s3["aws_secret_access_key"]
wasabi_bucket = cfg.s3["wasabi_bucket"]

s4 = boto3.client('s3',
endpoint_url = endpoint,
aws_access_key_id = aws_access_key,
aws_secret_access_key = aws_secret_key)

# if uploading tar.gz set type to application/gzip
#Upload a file and make it publicly available

def wasabiuploadfile(localfile,remotefile):
    s4.upload_file(
        localfile, wasabi_bucket, remotefile,
        ExtraArgs={
            'ACL': 'public-read', 
            'Metadata': 
            {
                'chain': 'waxtestnet',
                'version': '2.0.6'
            
            },
            'ContentType': 'application/gzip'
            }
    )

wasabiuploadfile('test.txt','test11.txt')
# Create the latest Snapshot
def createlatest(remotefile):
    s3 = boto3.resource('s3',
    endpoint_url = endpoint,
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key)
    s3.Object(wasabi_bucket,'snapshot-latest.tar.gz').copy_from(CopySource=wasabi_bucket+"/"+remotefile)

createlatest('test11.txt')

