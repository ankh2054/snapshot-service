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

ENV REPO="\
    deb [arch=amd64] https://apt.eossweden.org/wax bionic stable \
    deb [arch=amd64] https://apt.waxsweden.org/wax bionic testing \
"
## EOSswededn Package repostiory setup 
# Add GPG key
RUN wget --no-check-certificate -O- https://apt.eossweden.org/key 2> /dev/null | apt-key add -   
#RUN apt-add-repository -y 'deb [arch=amd64] https://apt.eossweden.org/wax bionic stable'    
#RUN apt-add-repository -y 'deb [arch=amd64] https://apt.waxsweden.org/wax bionic testing' 
## Add APT Repos
RUN for i in $REPO ; do sudo add-apt-repository -y $i; done
RUN apt update

RUN apt install -y $PACKAGES $WAX_BINARY && \
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
RUN wget --no-check-certificate -O- %SNAPSHOT_NAME
# From the snapshot URL get the filename and extract
RUN url=%SNAPSHOT_NAME; tar xzvf "${url##*/}"
# Change name of snapshot for use on EOS starting
RUN mv snapshot* snapshot-latest.bin


# Entrypoint
ADD start.sh /
RUN chmod u+x /start.sh
CMD /start.sh
                                            