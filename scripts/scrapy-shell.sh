if [ $# -ne 1 ]; then
  echo "usage: $0 <path to extracted html>"
  exit 1
fi

scrapy shell $1

