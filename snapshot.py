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

# Extract snapshot_name
SNAPSHOT_NAME = SNAPSHOT_INFO_JSON ['snapshot_name']
print(SNAPSHOT_NAME)

#Get current date and time
now = datetime.now()
# create date string for filename
dt_string = now.strftime("%d_%m_%Y-%H_%M")
# Create filename for snapshot using date string
FILENAME = 'snapshot' + dt_string+'.tar.gz'

# Compress the snapshot
subprocess.call(['tar', '-czf', FILENAME, SNAPSHOT_NAME])

wasabi.wasabiuploadfile(FILENAME,FILENAME,'waxtest2')
