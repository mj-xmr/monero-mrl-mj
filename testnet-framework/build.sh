#!/bin/bash -e

DIR_THIS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

DIR=/tmp/monero
PROJ=monero-mj
mkdir -p $DIR && cd $DIR

if [ ! -d $PROJ ]; then
	git clone https://github.com/mj-xmr/$PROJ.git 
	cd $PROJ
	git checkout mrl-fingerprint-fee
else
	cd $PROJ
fi

cp -v $DIR_THIS/Dockerfile .
sudo docker build .
