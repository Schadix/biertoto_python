#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd ${DIR}

. ../env/credentials

if [ "$#" -ne 1 ]; then
    echo "usage: $0 <spieltag>"
    exit 1
fi

cd ../biertoto/biertoto
export PYTHONPATH=`pwd`
OUTPUT_FOLDER="../../output"

mkdir -p $OUTPUT_FOLDER
scrapy crawl biertoto -L WARNING -a spieltag=$1 -a username=$USERNAME -a password=$PASSWORD -a tipprunde=watweissich -a tipper=Uwe,Schadix,TorstenFG -o $OUTPUT_FOLDER/spieltag-export-$1.csv -t biertoto

