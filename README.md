

1. Install Python (https://www.python.org/downloads/release/python-366/)
1. Install requirements (pip install -r requirements.txt)


Then 

```bash
cd ../biertoto/biertoto
export PYTHONPATH=`pwd`
OUTPUT_FOLDER="../../output"

mkdir -p $OUTPUT_FOLDER
scrapy crawl biertoto -a spieltag=$1 -a username=<username> -a password=<password> -o $OUTPUT_FOLDER/spieltag-export-$1.csv -t csv
```

