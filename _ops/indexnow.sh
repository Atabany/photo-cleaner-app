#!/bin/sh
# Notify IndexNow (Bing, Yandex, Seznam, Naver) about changed URLs.
#   sh _ops/indexnow.sh https://getphotocleaner.com/guides/x.html [more urls...]
KEY=745e7fc2fbb9e19f69d9371c6e3634be
[ $# -gt 0 ] || { echo "usage: $0 <url>..." >&2; exit 1; }
LIST=$(printf '"%s",' "$@" | sed 's/,$//')
curl -s -o /dev/null -w "IndexNow HTTP %{http_code}\n" -X POST https://api.indexnow.org/indexnow \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"host\":\"getphotocleaner.com\",\"key\":\"$KEY\",\"keyLocation\":\"https://getphotocleaner.com/$KEY.txt\",\"urlList\":[$LIST]}"
