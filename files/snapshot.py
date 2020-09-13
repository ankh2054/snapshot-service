import requests
import json
import time
from datetime import datetime
import subprocess
import wasabi



# SNAPSHOT END POINT
API_SNAPSHOT = 'http://127.0.0.1:8888/v1/producer/create_snapshot'


# Snapshot parameters
SNAPSHOT_DATA= {
"next": { "snapshot_name": "test" }
}

## Create snapshot and return filename + location
def create_snapshot():
    # Create the Snapshot using Producer API
    SNAPSHOT_INFO = requests.post(url=API_SNAPSHOT, json=SNAPSHOT_DATA)
    # Turn Response into JSON
    SNAPSHOT_INFO_JSON = json.loads(SNAPSHOT_INFO .text)
    # Extract snapshot_name full path  and filename snapshot-xxxxx.bin
    ## /chains/wax/snapshot-02484fb14bd426daeaf042eb8a02610c72f8c2db130f55f600eed6f4d47f6de7.bin
    SNAPSHOT_LOC = SNAPSHOT_INFO_JSON ['snapshot_name']
    return SNAPSHOT_LOC

## Get filename.bin of snapshot
def get_filename(snapshot_location):
    SNAPSHOT_NAME = snapshot_location
    # Extract snapshot bin filename only 
    ## Extract the position
    SNAPSHOT_FILENAME_POS = SNAPSHOT_NAME.find('snapshot-')
    ## Extract the string starting at position SNAPSHOT_FILENAME.POS
    SNAPSHOT_FILENAME = SNAPSHOT_NAME[SNAPSHOT_FILENAME_POS:]
    return SNAPSHOT_FILENAME 


def create_filename():
    #Get current date and time
    now = datetime.now()
    # create date string for filename
    dt_string = now.strftime("%d_%m_%Y-%H_%M")
    # Create filename for snapshot using date string
    FILENAME = 'snapshot-' + dt_string + '.tar.gz'
    return FILENAME
    

def main():
    # create new filename withdate timestamp and suffix of tar.gz 
    filename = create_filename()
    # Create snapshot and get location
    snapshot_loc = create_snapshot()
    # Get filename of snapshot by stripping location
    snapshot_filename = get_filename(snapshot_loc)
    # Mv the snapshot to current directory 
    subprocess.call([ 'mv', snapshot_loc, '.' ])
    # Create archive of snapshot filename
    subprocess.call(['tar', '-czf', filename, snapshot_filename])
    # Upload file to Wasabi
    wasabi.wasabiuploadfile(filename,filename)
    # Create latest file
    wasabi.createlatest(filename)
    # MV current snapshot to /eos/snapshots incase nodeos needs to restart
    subprocess.call([ 'rm', '/eos/snapshots/snapshot-latest.bin' ]) 
    subprocess.call([ 'mv', snapshot_filename, '/eos/snapshots/snapshot-latest.bin'])
    # delete snapshot 
    subprocess.call([ 'rm', filename ])

if __name__ == "__main__":
     main()
     
# Delete files older than 2 days in bucket specified
wasabi.delete_files()

