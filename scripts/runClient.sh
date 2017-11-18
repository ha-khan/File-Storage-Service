#!/bin/bash


if [ "$#" -ne 4 ]
then
	echo "Wrong arguments, usage :"
	echo "./runClient.sh <config_file> <base_dir> <command> <filename>"
	exit
fi

CONFIGFILE_PATH=$1
DOWNLOAD_DIR=$2
COMMAND=$3
FILENAME_OR_UPLOADDIR=$4


python /Users/hamzakhan/Desktop/CAREER/Projects/File-Storage-Service/src/Client.py $CONFIGFILE_PATH $DOWNLOAD_DIR $COMMAND $FILENAME_OR_UPLOADDIR
