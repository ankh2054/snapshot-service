![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)

# SNAPSHOT-DOCKER

This docker container:
- Sets up a running EOSIO process on the chain of your choosing.
- Install Python that takes a snapshot and pushes it to Amazon S3 or Wasabi
- Autorestarts on failures using the last snapshot taken.
- Prunes Snapshots on S3/Wasabi to only last 3 days worth.


## ENV Variables - These will make sense once you get into the Installation Part of the process.

|ENV & ARG                 |Value                          |Description                                   |
|--------------------------|---------------------------------------|--------------------------------------|
|**CHAIN_NAME**            |`wax`                                  | Used in P2P download from eosnation  |
|**SNAPSHOT_NAME**         |`http://x/snapshot.tar.gz`             | The initial snapshot to start with   |
|**WAX_BINARY**            |`wax-mv-206wax02`                      | Which package to install from APT    |
|**ENDPOINT_URL**          |`https://s3.eu-central-1.wasabisys.com`| Wasabi/S3 endpoint URL for downloads |
|**AWS_ACCESS_KEY_ID**     |`XXXXXXXXXXXXXXXX`                     | Wasabi/S3 access key        		  |
|**AWS_SECRET_ACCESS_KEY** |`XXXXXXXXXXXXXXXX`                     | Wasabi/S3 secret key 				  |
|**WASABI_BUCKET**         |`waxtest2`                     `       | Wasabi/S3 bucketname for snapshots   |



# Installation

## Requirements

- Docker 
- Brain 
- Coffee


## Step 1 - Build the docker container from github.

The first step is to buld the docker container from github 

**The following ENV variables need to be passed:**

- SNAPSHOT_NAME - The name of a snapshot to download that nodeos uses upon starting. This ensures your node syncs up to the network really fast.
- WAX_BINARY - Specifies the Nodeos APT package you want to install (See here for more details - https://eosswedenorg.github.io/apt/wax/bionic) :heart: to EOSsweden for the APT service. 
     
	 docker build  https://github.com/ankh2054/snapshot-service.git  \
	 -t snapshot.service \
	 --build-arg SNAPSHOT_NAME=https://snapshots.waxsweden.org/snapshots/57abfa/2.0/snapshot-65345117.bin.tar.gz \
	 --build-arg WAX_BINARY=wax-mv-206wax02 


**To Build it:**


**To run it:**

     docker run  --name snapshot.service.wax  -d  --expose 8888 \
	 -e 'CHAIN_NAME=wax' \
	 -e 'WAX_BINARY=wax-mv-206wax02' \
	 -e 'ENDPOINT_URL=https://s3.eu-central-1.wasabisys.com' \
	 -e 'AWS_ACCESS_KEY_ID=xxxxxxxxxxx' \
	 -e 'AWS_SECRET_ACCESS_KEY=xxxxxxxxxxx' \
	 -e 'WASABI_BUCKET=waxtest2' \
	 snapshot.service:latest


	

## ToDo

 - Automate APT sources to be installed