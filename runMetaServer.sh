#!/bin/bash


if [ "$#" -ne 2 ]
then
	echo "Wrong arguments, usage :"
	echo "./runMetaServer.sh <config_file> <id>"
	exit
fi

CONFIGFILE_PATH=$1
ID=$2


python MetadataServer.py $CONFIGFILE_PATH $ID

