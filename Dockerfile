#Download base image ubuntu 20.04
FROM ubuntu:18.04

LABEL maintainer="charles@sentnl.io"
LABEL version="0.1"
LABEL description="EOSIO + SNAPSHOT SERVICE."

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

ENV PACKAGES="\
  python3-pip \
  python3 \
  software-properties-common\
  supervisor \
  wget \
  nano \
  cron \
"
# To prevent - Warning: apt-key output should not be parsed (stdout is not a terminal)
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1


# Install required packages to add APT certifcate and APT REPOs
RUN apt update && apt install --no-install-recommends -y wget gnupg2 ca-certificates software-properties-common

## EOSswededn Package repostiory setup 
# Add GPG key
RUN wget --no-check-certificate -O- https://apt.eossweden.org/key 2> /dev/null | apt-key add -   
RUN apt-add-repository -y 'deb [arch=amd64] https://apt.eossweden.org/wax bionic stable'    
RUN apt-add-repository -y 'deb [arch=amd64] https://apt.waxsweden.org/wax bionic testing' 


# Pull in build argument
ARG WAX_BINARY
# Install Packages including WAX_BINARY
RUN apt update && apt install --no-install-recommends -y $PACKAGES $WAX_BINARY && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

# Setup Directories
RUN mkdir -p /eos/snapshots

# Add files
ADD files/snapshot.py /eos/snapshot.py
ADD files/wasabi.py /eos/wasabi.py
ADD files/requirements.txt /eos/requirements.txt
ADD files/cron-snapshot /etc/cron.d

# Permissions
RUN chmod 0644 /etc/cron.d/cron-snapshot

# Get latest snapshot
WORKDIR /eos/snapshots
# Pull in build argument
ARG SNAPSHOT_NAME 
RUN wget --no-check-certificate  $SNAPSHOT_NAME
# From the snapshot URL get the filename and extract
RUN url=$SNAPSHOT_NAME; tar xzvf "${url##*/}"
# Change name of snapshot for use on EOS starting
RUN mv snapshot*.bin snapshot-latest.bin

# Entrypoint
ADD files/start.sh /
RUN chmod u+x /start.sh
CMD /start.sh
                                            