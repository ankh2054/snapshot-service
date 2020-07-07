![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)

# SNAPSHOT-DOCKER

snapshot-docker sets up a container running EOSIO on the chain of your choosing.


To buld the docker modx image:
docker build https://github.com/ankh2054/flask-docker-nginx.git -t snapshot.service

## ENV Variables

|ENV                       |Value                          |Description                                   |
|--------------------------|---------------------------------------|--------------------------------------|
|**CHAIN_NAME**            |`wax`                                  |'Used in P2P download from eosnation' |
|**SNAPSHOT_NAME**         |`http://x/snapshot.tar.gz`             |"The initial snapshot to start with"  |
|**WAX_BINARY**            |`wax-mv-206wax02`                      |'Which packe to install from APT'     |
|**ENDPOINT_URL**          |`https://s3.eu-central-1.wasabisys.com`|'Wasabi/S3 endpoint URL for downloads'|
|**AWS_ACCESS_KEY_ID**     |`XXXXXXXXXXXXXXXX`                     |"Wasabi/S3 access key"        		  |
|**AWS_SECRET_ACCESS_KEY** |`XXXXXXXXXXXXXXXX`                     |'Wasabi/S3 secret key 				  |
|**WASABI_BUCKET**         |`waxtest2                     `        |Wasabi/S3 bucketname for snapshots    |

- **CHAIN_NAME**=wax ( the chain used where P2P list is dowlonaded from eosnation validation)
- **SNAPSHOT_NAME**=https://s3.eu-central-1.wasabisys.com/waxtest2/snapshot-latest.tar.gz   (the initial snapshot to start nodeos with)
- **WAX_BINARY**=wax-mv-206wax02 ( the package to be installed from APT )
- **ENDPOINT_URL**=https://s3.eu-central-1.wasabisys.com ( Wasabi/S3 endpoint URL for downloads )
- **AWS_ACCESS_KEY_ID**=xxxxxxxxxxx ( Wasabi/S3 access key  )
- **AWS_SECRET_ACCESS_KEY**=xxxxxxxxxxx ( Wasabi/S3 secret key  )
- **WASABI_BUCKET**=waxtest2 ( Wasabi/S3 bucketname where snapshots will be saved  )

To run it:

    $ docker run  --name snapshot.service.wax  -d \
	 -e 'CHAIN_NAME=wax' \
	 -e 'SNAPSHOT_NAME=https://s3.eu-central-1.wasabisys.com/waxtest2/snapshot-latest.tar.gz' \
	 -e 'WAX_BINARY=wax-mv-206wax02' \
	 -e 'ENDPOINT_URL=https://s3.eu-central-1.wasabisys.com' \
	 -e 'AWS_ACCESS_KEY_ID=xxxxxxxxxxx' \
	 -e 'AWS_SECRET_ACCESS_KEY=xxxxxxxxxxx' \
	 -e 'WASABI_BUCKET=waxtest2' \
	 snapshot.service

