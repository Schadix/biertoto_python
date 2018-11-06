

1. Install Python (https://www.python.org/downloads/release/python-366/)
1. Install requirements (pip install -r requirements.txt)


Then 

```bash
cd ../biertoto/biertoto
export PYTHONPATH=`pwd`
OUTPUT_FOLDER="../../output"

mkdir -p $OUTPUT_FOLDER
scrapy crawl biertoto -a spieltag=$1 -a username=<username> -a password=<password> -a tipper=Uwe,Schadix,TorstenFG -a tipprunde=watweissich -o $OUTPUT_FOLDER/spieltag-export-$1.csv -t biertoto
```

