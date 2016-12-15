
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

    basequery=dict( fq=[ 'sourceId:"dpa"',
                         'language:"de"' ],
                wt="json",
                rows=10,
                sort="createdAt desc",
                omitHeader="true",
                fl="createdAt,dpaId,dpaTitle,id,sectors,dpaText")

    # basequery["fq"].extend(blacklist)


    startdate=datetime.datetime.now()-datetime.timedelta(days=1)
    days=1

    branchen=json.load(open("branchen.json"),object_pairs_hook=OrderedDict)

    rootlabel="Branchennews dpa"
    directory="../html/data/demo-dpa"
    rootfile="index.json"
    indexfile="{date:%Y%m%d}-index.json"
    indexlabel="{date:%d. %m. %Y}"
    docfile="{date:%Y%m%d}/{doc[id]}.json"

    rename=[('dpaTitle',       'title'),
            ('dpaText',        'text')
            ]


    template={
      "placeholder": "Korrekte Branche",
      "subject": "Branchendienst dpa - Feedback",
      "email": "mvirtel@dpa-newslab.com",
      "description": "<h2>Anleitung</h2><p>Unser Algorithmus hat sich als Redakteur versucht und Meldungen bei der dpa gesucht, die zu den Branchen passen. Bitte markieren Sie alle Nachrichten, die nicht in die dargestellte Branche passen. <a href='#'>Mehr Informationen zu diesem Experiment</a></p>",
      "title": "Branchendienst - dpa"
    	}

    filter=lambda a: not re.search(r"\bdpa-AFX\b",a["text"])


if __name__=="__main__" :
    generate(Config)






