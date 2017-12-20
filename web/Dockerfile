FROM ubuntu:16.04

# Initialize
RUN mkdir -p /data/web
WORKDIR /data/web
COPY requirements.txt /data/web/

# Setup
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y  python3 python3-dev postgresql-client postgresql-server-dev-all \
                        gettext openssh-server libxml2-dev  libffi-dev libxslt-dev curl apt-utils \
                        git htop man unzip vim wget python3-pip python3-gunicorn gunicorn3 && \
    rm -rf /var/lib/apt/lists/* 
RUN pip3 install --upgrade pip
RUN pip3 install certifi fake_useragent bs4 requests
RUN pip3 install -r requirements.txt
RUN wget https://dist.ipfs.io/go-ipfs/v0.4.13/go-ipfs_v0.4.13_linux-amd64.tar.gz -qO-|tar xz && cd go-ipfs && ./install.sh &&cd ../ && rm -rf go-ipfs
RUN ln -s /usr/bin/gunicorn3 /usr/bin/gunicorn

# Prepare
COPY . /data/web/
RUN mkdir -p sljweb/static/admin
