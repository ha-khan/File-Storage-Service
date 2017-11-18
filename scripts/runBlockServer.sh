#!/bin/bash


if [ "$#" -ne 1 ]
then
	echo "Wrong arguments, usage :"
	echo "./runBlockServer.sh <config_file>"
	exit
fi


CONFIGFILE_PATH=$1

python /Users/hamzakhan/Desktop/CAREER/Projects/File-Storage-Service/src/BlockServer.py $CONFIGFILE_PATH
