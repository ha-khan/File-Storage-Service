#!/bin/bash

if [ "$#" -ne 1 ]
then
	echo "Wrong arguments, usage :"
	echo "./build.sh <build or clean>"
	exit
fi

BUILD_OR_CLEAN=$1

if [ $BUILD_OR_CLEAN == "build" ]
then
	echo "Building"
	thrift --gen py -r metadataServer.thrift
	thrift --gen py -r blockServer.thrift
    thrift --gen py -r shared.thrift

	exit

elif [ $BUILD_OR_CLEAN == "clean" ]
then
	echo "Cleaning"
	rm -rf gen-py

else
	echo "Wrong build command"
	echo "Either ./build.sh build or ./build.sh clean"
	exit
fi