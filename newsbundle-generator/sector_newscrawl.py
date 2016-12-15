
# coding: utf-8

# # Get 12 Hours of Sample News from neofonie

import sys
import logging
import re
import datetime
import json
from bundler import generate
from collections import OrderedDict

logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)

logger=logging.getLogger(__name__)


# CONFIG

class Config :
    blacklist={'-neoApplication:"{0}"'.format(a) for a in re.findall(r"\S+","""
    adhoc_news freiepresse firmenpresse presseportal shortnews news4press
    finanznachrichten fair_news_de artikel_presse_de prcenter_de aktiencheck
    """)}

    basequery=dict( fq=[ 'sourceId:"neofonie"',
                         'language:"de"' ],
                    wt="json",
                    rows=10,
                    sort="createdAt desc",
                    omitHeader="true",
                    fl="createdAt,neoTeaser,neoTitle,neoUrl,id,neoApplication,sectors,text,neoBaseUrl")

    basequery["fq"].extend(blacklist)


    startdate=datetime.datetime.now()-datetime.timedelta(days=1)
    days=1

    branchen=json.load(open("branchen.json"),object_pairs_hook=OrderedDict)

    rootlabel="Branchennews"
    directory="../html/data/demo-newscrawl"
    rootfile="index.json"
    indexfile="{date:%Y%m%d}-index.json"
    indexlabel="{date:%d. %m. %Y}"
    docfile="{date:%Y%m%d}/{doc[id]}.json"

    rename=[('neoTitle',       'title'),
            ('neoApplication', 'source'),
            ('neoTeaser',      'subtitle'),
            ('neoUrl',          'sourcelink')
            ]


    template={
      "placeholder": "Korrekte Branche",
      "subject": "Branchendienst Newscrawl - Feedback",
      "email": "mvirtel@dpa-newslab.com",
      "description": "<h2>Anleitung</h2><p>Unser Algorithmus hat sich als Redakteur versucht und Meldungen im Internet gesucht, die zu den Branchen passen. Bitte markieren Sie alle Nachrichten, die nicht in die dargestellte Branche passen. <a href='#'>Mehr Informationen zu diesem Experiment</a></p>",
      "title": "Branchendienst - Newscrawl"
    	}

    filter=lambda a: not re.search(r"\bdpa\b",a["text"])


if __name__=="__main__" :
    generate(Config)






