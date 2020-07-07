#!/bin/sh

# Creating supervisor file
###########################
## ENV variables can be passed as ${DJANGO_APP_NAME}

create_supervisor_conf() {
echo "Creating supervisor.conf"
  rm -rf /etc/supervisord.conf
  cat > /etc/supervisord.conf <<EOF
[unix_http_server]
file=/var/run/supervisor.sock   ; 
chmod=0700                       ; 
[supervisord]
logfile=/var/log/supervisord.log ; 
pidfile=/var/run/supervisord.pid ; 
childlogdir=/var/log/           ; 
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
[supervisorctl]
serverurl=unix:///var/run/supervisor.sock ; 

[program:eosio]
command=/usr/opt/wax-mv/${WAX_BINARY}/bin/nodeos --data-dir /eos --config-dir /eos --snapshot=snapshots/snapshot-latest.bin
numprocs=1
autostart=true

[program:crond]
priority = 100
command = bash -c "while true; do sleep 0.1; [[ -e /var/run/crond.pid ]] || break; done && exec /usr/sbin/crond -m off -n"
startsecs = 0
autorestart = true
redirect_stderr = true
stdout_logfile = /var/log/cron
stdout_events_enabled = true

EOF
}


create_config_ini() {
cd /eos/
echo "Creating EOS config.ini"

  cat > config.ini <<EOF
# host:port for incoming p2p connections.
p2p-listen-endpoint = 0.0.0.0:9876
http-server-address = 0.0.0.0:8888
chain-state-db-size-mb = 16768
chain-state-db-guard-size-mb = 256
reversible-blocks-db-size-mb = 2048
reversible-blocks-db-guard-size-mb = 16
wasm-runtime = eos-vm-jit
max-clients = 50
p2p-max-nodes-per-host = 10
sync-fetch-span = 500
snapshots-dir = "/chains/wax/snapshots"
plugin = eosio::chain_api_plugin
plugin = eosio::chain_plugin
plugin = eosio::db_size_api_plugin
plugin = eosio::producer_api_plugin
EOF

# Download the P2P report and add to config.ini
echo "Downloading P2P lsit and adding to config.ini"

wget https://validate.eosnation.io/${CHAIN_NAME}/reports/config.txt
cat config.txt >> config.ini
}

python_snapshot_setup() {

echo "Installing python packages"
# Install python packages
pip3 install --no-cache-dir -r /eos/requirements.txt

# Creating the wasabiconfig.py env variables
echo "Creating the wasabiconfig.py env variables"

  cat > wasabiconfig.py <<EOF
#!/usr/bin/env python
import preprocessing

s3 = 
    "endpoint_url": ${ENDPOINT_URL,
    "aws_access_key_id": ${AWS_ACCESS_KEY_ID},
    "aws_secret_access_key": ${AWS_SECRET_ACCESS_KEY},
    "wasabi_bucket": ${WASABI_BUCKET}
}
EOF
}

# Running all our scripts
create_supervisor_conf
create_config_ini
python_snapshot_setup

# Start Supervisor 
echo "Starting Supervisor"
/usr/bin/supervisord -n -c /etc/supervisord.conf
