
![SVG logo](https://www.sentnl.io/sentnl.svg)
          ![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)

# Sentnl.io  








# Automated Snapshot Service for WAX

**This docker container:**

1. Sets up a running EOSIO process on the chain of your choosing.
2. Install Python that takes hourly snapshots and pushes them Amazon S3 or Wasabi.
3. Autorestarts on failures using the last snapshot taken.
4. Prunes Snapshots on S3/Wasabi to only keep last 3 days.

:pound: NOTE that Wasabi only costs £5 pcm for 1TB :pound:

**ENV Variables - These will make sense once you get into the Installation Part of the process.**

|ENV & ARG                 |Value                          |Description                                   |
|--------------------------|---------------------------------------|--------------------------------------|
|**CHAIN_NAME**            |`wax`                                  | Used in P2P download from eosnation  |
|**SNAPSHOT_NAME**         |`http://x/snapshot.tar.gz`             | The initial snapshot to start with   |
|**WAX_BINARY**            |`wax-mv-206wax02`                      | Which package to install from APT    |
|**ENDPOINT_URL**          |`https://s3.eu-central-1.wasabisys.com`| Wasabi/S3 endpoint URL for downloads |
|**AWS_ACCESS_KEY_ID**     |`XXXXXXXXXXXXXXXX`                     | Wasabi/S3 access key        		  |
|**AWS_SECRET_ACCESS_KEY** |`XXXXXXXXXXXXXXXX`                     | Wasabi/S3 secret key 				  |
|**WASABI_BUCKET**         |`waxtest2`                     `       | Wasabi/S3 bucketname for snapshots   |



# Installation Steps to get started

## Installation Requirements

- Docker 
- Amazon S3 account or Wasabi
- Coffee

## Step 1 - Setup your Amazon S3 or Wasabi account.


1. Setup a Amnazon S3 or Wasabi account
	* https://wasabi.com
	* https://aws.amazon.com/s3/
2. Create a bucket. (Remember the name)
3. Create your API keys. Make sure they have permissions to read and write to the bucket.

## Step 2 - Build the docker container from github.

The first step is to buld the docker container from github 

### The following ENV variables need to be passed:

- **SNAPSHOT_NAME** - The URL link of a snapshot to download that nodeos uses upon starting. This ensures your node syncs up to the network really fast. :exclamation: Only tar.gz is currently supported.
- **WAX_BINARY** - Specifies the Nodeos APT package you want to install (See here for more details - https://eosswedenorg.github.io/apt/wax/bionic) :heart: to EOSsweden for the APT service. 

**To build it:**
     
	 docker build  https://github.com/ankh2054/snapshot-service.git  \
	 -t snapshot.service \
	 --build-arg SNAPSHOT_NAME=https://snapshots.waxsweden.org/snapshots/57abfa/2.0/snapshot-68153023.bin.tar.gz \
	 --build-arg WAX_BINARY=wax-mv-206wax02 



## Step 3 - Running the docker container.

The final step is to start the container. 

### The following ENV variables need to be passed:

- **CHAIN_NAME** - The name of the chain to take snapshots for. :exclamation: Please note that only WAX is currently supported.
- **WAX_BINARY** - Specifies the Nodeos APT package you want to install (See here for more details - https://eosswedenorg.github.io/apt/wax/bionic) :heart: to EOSsweden for the APT service. 
- **ENDPOINT_URL** - The Wasabi/S3 endpoint URL for your buckets These can be found within your S3/Wasabni control panels.
- **AWS_ACCESS_KEY_ID** - Your Wasabi/S3 API access key 
- **AWS_SECRET_ACCESS_KEY** - Your Wasabi/S3 API secret key 
- **WASABI_BUCKET** - The name of your bucket where to files will be uploaded to.

**To run it:**

```Dockerfile
docker run  --name snapshot.service.wax  -d  --expose 8888 \
-e 'CHAIN_NAME=wax' \
-e 'WAX_BINARY=wax-mv-206wax02' \
-e 'ENDPOINT_URL=https://s3.eu-central-1.wasabisys.com' \
-e 'AWS_ACCESS_KEY_ID=xxxxxxxxxxx' \
-e 'AWS_SECRET_ACCESS_KEY=xxxxxxxxxxx' \
-e 'WASABI_BUCKET=waxtest2' \
snapshot.service:latest
```

### That is it - the service will now take hourly snapshots for you.

In the next coming weeks we will be creating a frontend for the service to display the available snapshots.

### Troubleshooting 

* You can check the container is running without any errors. 

```docker logs snapshot.service.wax```


* Check nodeos is running on your container. Note that this takes 2-3 minutes to sync up once you start the container.

```curl http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' snapshot.service.wax):8888/v1/chain/get_info```

* Technically there is no need to expose port 8888, but it's there incase you want to monitor this node with your monitoring system. If you dont run intend on monitoring the service remove the `--expose` option during the container run. 

## ToDo

1. Automate APT sources to be installed
2. Setup ENV for python pruning setting in days.
3. Create Automated frontend pulling SVG logos from wax.json
4. Change container to run as specific user called snapshot and not root