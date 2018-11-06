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
scrapy crawl biertoto -L INFO -a spieltag=$1 -a username=$USERNAME -a password=$PASSWORD -a tipprunde=tipp469 -a tipper=up1967,UweS,Heiko,Master78,UweM -o $OUTPUT_FOLDER/spieltag-export-tipp469-$1.csv -t biertoto

