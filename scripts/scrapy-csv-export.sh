#!/usr/bin/env bash
. ../env/credentials

if [ "$#" -ne 1 ]; then
    echo "usage: $0 <spieltag>"
    exit 1
fi

cd ../biertoto/biertoto
export PYTHONPATH=`pwd`
OUTPUT_FOLDER="../../output"

mkdir -p $OUTPUT_FOLDER
scrapy crawl biertoto -a spieltag=$1 -a username=$USERNAME -a password=$PASSWORD -o $OUTPUT_FOLDER/spieltag-export-$1.csv -t csv

