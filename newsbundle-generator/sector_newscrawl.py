
# coding: utf-8

# # Get 12 Hours of Sample News from neofonie

import sys
import logging
import re
import datetime
import json
from bundler import generate
from collections import OrderedDict
import os
logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)

logger=logging.getLogger(__name__)

_HERE=os.path.split(__file__)[0]

# CONFIG

class Config :
    blacklist={'-neoApplication:"{0}"'.format(a) for a in re.findall(r"\S+","""
    adhoc_news freiepresse firmenpresse presseportal shortnews news4press
    finanznachrichten fair_news_de artikel_presse_de prcenter_de aktiencheck
    """)}

    basequery=dict( fq=[ 'sourceId:"neofonie"',
                         'language:"de"' ],
                    wt="json",
                    rows=190,
                    sort="createdAt desc",
                    omitHeader="true",
                    fl="createdAt,neoTeaser,neoTitle,neoUrl,id,neoApplication,sectors,text,neoBaseUrl")

    basequery["fq"].extend(blacklist)


    startdate=datetime.datetime.now()-datetime.timedelta(days=1)
    days=5

    branchen=json.load(open(os.path.join(_HERE,"branchen.json")),object_pairs_hook=OrderedDict)

    rootlabel="Branchennews"
    directory=os.path.join(_HERE,"../html/data/demo-newscrawl")
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
      "description": "<h2>Anleitung</h2><p>Unser Algorithmus hat sich beim Nachrichtensortieren versucht und Meldungen aus dem deutschen Internet den Branchen von dpa-AFX zugeordnet. <br/> Wie gut hat das geklappt? Das müssen wir mit menschlicher Intelligenz herausfinden. Bitte markieren Sie alle Nachrichten, die nicht in die dargestellte Branche passen, und schreiben Sie ggf. dazu, welche Branche es hätte sein sollen. <!-- <a href=''>Mehr Informationen zu diesem Experiment</a>--> </p>",
      "title": "News-Stream Branchendienst - Internet",

    	}

    filter=lambda a: not re.search(r"\b(dpa|DGAP-News)\b",a["text"])


if __name__=="__main__" :
    generate(Config)






