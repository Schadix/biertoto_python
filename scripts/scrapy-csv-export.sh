#!/usr/bin/env bash
. ../env/credentials

cd /Users/schadem/code/github/schadix/biertoto_python/biertoto/biertoto
export PYTHONPATH=`pwd`


scrapy crawl biertoto -a spieltag=1 -a username=$USERNAME -a password=$PASSWORD -o spieltag-export-2.csv -t csv

