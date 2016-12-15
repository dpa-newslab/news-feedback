
# coding: utf-8

# # Get 12 Hours of Sample News from neofonie

# In[ ]:
import pipe
import datapipeline
import neofonie
import json
from collections import OrderedDict
import re
import copy
import os
import sys
import datetime
import logging
from functools import reduce

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
                    fl="createdAt,neoTeaser,neoTitle,neoUrl,id,neoApplication,sectors,text")

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
            ('neoUrl',          'url')
            ]


    template={
      "placeholder": "Korrekte Branche",
      "subject": "Branchendienst Newscrawl - Feedback",
      "email": "mvirtel@dpa-newslab.com",
      "description": "<h2>Anleitung</h2><p>Unser Algorithmus hat sich als Redakteur versucht und Meldungen im Internet gesucht, die zu den Branchen passen. Bitte markieren Sie alle Nachrichten, die nicht in die dargestellte Branche passen. <a href='#'>Mehr Informationen zu diesem Experiment</a></p>",
      "title": "Branchendienst - Newscrawl"
    	}


# End Config



def mkdirs_and_open(f,*args) :
    (p,n)=os.path.split(f)
    if not os.path.exists(p) :
        os.makedirs(p)
    return open(f,*args)


def generate(config) :
    texts={}
    docs=OrderedDict()
    for day in range(0,config.days) :
        date=config.startdate-datetime.timedelta(days=day)
        label=config.indexlabel.format(**locals())
        results=OrderedDict()
        indexfilename=config.indexfile.format(**locals())
        docs[label]=indexfilename
        dayquery=copy.deepcopy(config.basequery)
        dayquery["fq"].append(date.strftime('createdAt:[%Y-%m-%dT00:00:00.000Z TO %Y-%m-%dT23:59:59.999Z]'))
        for (k,n) in config.branchen.items() :
            nq=copy.deepcopy(dayquery)
            nq["fq"].append('sectors:"{0}"'.format(k))
            res=list(neofonie.query("*",**nq)["response"]["docs"] | pipe.where(lambda a: not re.search(r"\bdpa\b",a["text"]))
                    | datapipeline.rename_attributes(Config.rename)
                    | datapipeline.deduplicate(key=lambda a: a["title"] ) )
            logging.debug("Sector: %s - %s - %s docs" % (k,date.strftime("%Y-%m-%d"),len(res)))
            if len(res)>0 :
                results[k]=dict(docs=res,label=n)
        for nr in results.values() :
            for doc in nr["docs"] :
                filename=config.docfile.format(**locals())
                doc["document"]=filename
                ndoc=copy.deepcopy(doc)
                ndoc["index"]=os.path.join("..",indexfilename)
                ndoc["sector"]=doc["sectors"][0]
                ndoc["root"]=os.path.join("..",config.rootfile)
                ndoc["source"]="ex neoApplication"
                ndoc["sourcelink"]="ex neoURL"
                ndoc["subtitle"]="Untertitel zu {}".format(ndoc.get("title","---"))
                texts[os.path.join(config.directory,filename)]=ndoc
                if "text" in doc :
                    del(doc["text"])

        with mkdirs_and_open(os.path.join(config.directory,indexfilename),"w") as of :
            json.dump(dict(news=results,root=config.rootfile,rootlabel=config.rootlabel),of)
            logging.info("%s items written to %s" %
                         (reduce(lambda a,b: a+b,(len(a["docs"]) for a in results.values()),0), of.name))



    for (k,v) in texts.items() :
        json.dump(v,mkdirs_and_open(k,"w"))
    logging.debug("%s news objects written" % len(list(texts.keys())))
    t=copy.deepcopy(Config.template)
    t["chapters"]=docs
    json.dump(t,open(os.path.join(config.directory,config.rootfile),"w"))




# In[2]:

generate(Config)



# In[7]:



