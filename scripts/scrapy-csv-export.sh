#!/usr/bin/env bash
. ../env/credentials

if [ "$#" -ne 1 ]; then
    echo "usage: $0 <spieltag>"
    exit 1
fi

cd /Users/schadem/code/github/schadix/biertoto_python/biertoto/biertoto
export PYTHONPATH=`pwd`

scrapy crawl biertoto -a spieltag=$1 -a username=$USERNAME -a password=$PASSWORD -o ../../../output/spieltag-export-2.csv -t csv

