
# coding: utf-8

# # Get 12 Hours of Sample News from neofonie

import sys
import logging
import re
import datetime
import json
import os
from bundler import generate
from collections import OrderedDict

logging.basicConfig(stream=sys.stderr,level=logging.DEBUG,
                    format='%(levelname)s %(filename)s:%(lineno)s %(message)s')

logger=logging.getLogger(__name__)

_HERE=os.path.split(__file__)[0]
# CONFIG

class Config :
    blacklist={'-neoApplication:"{0}"'.format(a) for a in re.findall(r"\S+","""
    adhoc_news freiepresse firmenpresse presseportal shortnews news4press
    finanznachrichten fair_news_de artikel_presse_de prcenter_de aktiencheck
    """)}

    basequery=dict( fq=[ 'sourceId:"dpa"',
                         'language:"de"' ],
                wt="json",
                rows=190,
                sort="createdAt desc",
                omitHeader="true",
                fl="createdAt,dpaId,dpaTitle,id,sectors,dpaText")

    # basequery["fq"].extend(blacklist)


    startdate=datetime.datetime.now()-datetime.timedelta(days=1)
    days=5

    branchen=json.load(open(os.path.join(_HERE,"branchen.json")),object_pairs_hook=OrderedDict)

    rootlabel="Branchennews dpa"
    directory=os.path.join(_HERE,"../html/data/demo-dpa")
    rootfile="index.json"
    indexfile="{date:%Y%m%d}-index.json"
    indexlabel="{date:%d. %m. %Y}"
    docfile="{date:%Y%m%d}/{doc[id]}.json"

    rename=[('dpaTitle',       'title'),
            ('dpaText',        'text')
            ]


    template={
      "placeholder": "Falsch !",
      "subject": "Branchendienst dpa - Feedback",
      "email": "mvirtel@dpa-newslab.com",
      "description": "<h2>Anleitung</h2><p>Unser Algorithmus hat sich beim Nachrichtensortieren versucht und Meldungen aus der dpa-Berichterstattung den Branchen von dpa-AFX zugeordnet. <br/> Wie gut hat das geklappt? Das müssen wir mit menschlicher Intelligenz herausfinden. Bitte markieren Sie alle Nachrichten, die nicht in die dargestellte Branche passen, und schreiben Sie ggf. dazu, welche Branche es hätte sein sollen. <!-- <a href=''>Mehr Informationen zu diesem Experiment</a>--> </p>",
      "title": "News-Stream Branchendienst - dpa"
    	}

    filter=lambda a: not re.search(r"dpa-AFX|DGAP",a.get("title")+a.get("text")) \
                     and not re.search(r"\s*\*",a["title"])

if __name__=="__main__" :
    generate(Config)






