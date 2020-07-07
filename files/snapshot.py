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

# Create the Snapshot using Producer API
SNAPSHOT_INFO = requests.post(url=API_SNAPSHOT, json=SNAPSHOT_DATA)

# Turn Response into JSON
SNAPSHOT_INFO_JSON = json.loads(SNAPSHOT_INFO .text)

# Extract snapshot_name full path  and filename
SNAPSHOT_NAME = SNAPSHOT_INFO_JSON ['snapshot_name']
print(SNAPSHOT_NAME)

# Extract snapshot bin filename only 
## Extract the position
SNAPSHOT_FILENAME_POS  = SNAPSHOT_NAME.find('snapshot-')
## Extract the strign starting at position SNAPSHOT_FILENAME.POS
SNAPSHOT_FILENAME = SNAPSHOT_NAME[SNAPSHOT_FILENAME_POS:]

#Get current date and time
now = datetime.now()
# create date string for filename
dt_string = now.strftime("%d_%m_%Y-%H_%M")
# Create filename for snapshot using date string
FILENAME = 'snapshot-' + dt_string + '.tar.gz'

# Mv the snapshot to current directory 
subprocess.call([ 'mv', SNAPSHOT_NAME, '.' ])
# Create archive of snapshot filename
subprocess.call(['tar', '-czf', FILENAME, SNAPSHOT_FILENAME])
# delete snapshot 
subprocess.call([ 'rm', SNAPSHOT_FILENAME ])

# Upload file to Wasabi
wasabi.wasabiuploadfile(FILENAME,FILENAME)
# Create latest file
wasabi.createlatest(FILENAME)

# MV current snapshot to /eos/snapshots incase nodeos needs to restart
subprocess.call([ 'rm', '/eos/snapshots/snapshot-*.*' ]) 
subprocess.call([ 'mv', SNAPSHOT_FILENAME, '/eos/snapshots/snapshot-latest.bin'])


