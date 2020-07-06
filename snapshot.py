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

# Compress the snapshot
subprocess.call([ 'mv', SNAPSHOT_NAME, '.' ])
subprocess.call(['tar', '-czf', FILENAME, SNAPSHOT_FILENAME])

#Upload file to Wasabi
wasabi.wasabiuploadfile(FILENAME,FILENAME,'waxtest2')