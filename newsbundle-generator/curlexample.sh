#! /bin/bash

curl -u $USER:$PASSWORD -G -g 'https://nstr.neofonie.de/solr-dev/news/select' \
                              --data-urlencode 'q=*:*' \
                              --data-urlencode 'wt=json' \
                              --data-urlencode 'fq=createdAt:[NOW/HOUR-24HOUR TO NOW/HOUR+1HOUR]' \
                              --data-urlencode 'fq=sourceId:"dpa"' \
                              --data-urlencode 'fq=labels:"Kriminalität"' \
                              --data-urlencode 'sort=createdAt desc'
