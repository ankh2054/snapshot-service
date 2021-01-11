#Download base image ubuntu 20.04
FROM ubuntu:18.04

LABEL maintainer="charles@sentnl.io"
LABEL version="1.0"
LABEL description="EOSIO MULTICHAIN SNAPSHOT SERVICE."

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive


# Add EOS user
RUN groupadd --gid 1001 eos \
   && useradd --uid 1001 --gid 1001 --shell /bin/bash --create-home --home /home/eos eos


## Start Runninng as ROOT ##
ENV PACKAGES="\
  python3-pip \
  python3 \
  supervisor \
  nano \
  cron \
  python3-setuptools \
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
RUN mkdir -p /eos/snapshots && \
    mkdir -p /eos/supervisor/log && \
    mkdir -p /eos/cron && \
    chown eos:eos -R /eos/

#ADD files/cron-snapshot /etc/cron.d

# Permissions and add cron to snapshot crontab
#RUN chmod 0644 /etc/cron.d/cron-snapshot && crontab /etc/cron.d/cron-snapshot



# Change to eos user
USER eos

# Get latest snapshot
WORKDIR /eos/snapshots
# Pull in build argument
ARG SNAPSHOT_NAME 
RUN wget --no-check-certificate  $SNAPSHOT_NAME
# From the snapshot URL get the filename and extract
RUN filename=$SNAPSHOT_NAME; tar xzvf "${filename##*/}"
# Change name of snapshot for use on EOS starting
RUN mv snapshot*.bin snapshot-latest.bin
# Remove original snapshot download
RUN rm snapshot*.tar.gz 


# Add files
WORKDIR /eos
ADD files/start.sh entry/.
ADD files/snapshot.py .
ADD files/wasabi.py .
ADD files/requirements.txt .
ADD files/cron-snapshot cron/.

# Changing back to root to change permissions, normal user cannot.
USER root
WORKDIR /eos 
RUN chown eos:eos snapshot.py && \
    chown eos:eos wasabi.py && \
    chown eos:eos requirements.txt && \
    chmod u+x entry/start.sh && chown eos:eos entry/start.sh

# Setup crontask for user EOS
RUN chmod 0644 /eos/cron/cron-snapshot && \
    chown eos:eos /eos/cron/cron-snapshot && \
    crontab -u eos /eos/cron/cron-snapshot 


# Change back to EOS user to start processes.
USER eos
CMD /eos/entry/start.sh
                                            