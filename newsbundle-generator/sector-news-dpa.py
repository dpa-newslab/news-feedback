
# coding: utf-8

# # Get 12 Hours of Sample News from dpa

# In[ ]:

from neofonie import query,deduplicate,filter_response
import json
from collections import OrderedDict
branchen=json.load(open("branchen.json"),object_pairs_hook=OrderedDict)
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

blacklist={'-neoApplication:"{0}"'.format(a) for a in re.findall(r"\S+","""
adhoc_news freiepresse firmenpresse presseportal shortnews news4press
finanznachrichten fair_news_de artikel_presse_de prcenter_de aktiencheck
""")}

basequery=dict( fq=[ 'sourceId:"dpa"',
                     'language:"de"' ],
                wt="json",
                rows=90,
                sort="createdAt desc",
                omitHeader="true",
                fl="createdAt,dpaId,dpaTitle,neoUrl,id,sectors,dpaText")

basequery["fq"].extend(blacklist)


startdate=datetime.datetime.now()

days=8


directory="sectors-source-dpa/v3"
rootfile="index.json"
indexfile="{date:%Y%m%d}-index.json"
indexlabel="{date:%d. %m. %Y}"
docfile="{date:%Y%m%d}/{doc[id]}.json"

textAttribute="dpaText"
deduplicateAttribute="dpaId"

attributeNames={ 'sectors' : 'sections',
                 'sector'  : 'section',
                 'dpaId'   : 'externalId',
                 'dpaTitle' : 'title',
                 'dpaText'  : 'text'
               }


filtertext= ("dpa-AFX")



# End Config

texts={}
docs=OrderedDict()


def mkdirs_and_open(f,*args) :
    (p,n)=os.path.split(f)
    if not os.path.exists(p) :
        os.makedirs(p)
    return open(f,*args)



for day in range(1,days) :
    date=startdate-datetime.timedelta(days=day)
    label=indexlabel.format(**locals())
    results=OrderedDict()
    indexfilename=indexfile.format(**locals())
    docs[label]=indexfilename
    dayquery=copy.deepcopy(basequery)
    dayquery["fq"].append(date.strftime('createdAt:[%Y-%m-%dT00:00:00.000Z TO %Y-%m-%dT23:59:59.999Z]'))
    for (k,n) in branchen.items() :
        nq=copy.deepcopy(dayquery)
        nq["fq"].append('sectors:"{0}"'.format(k))
        res=filter_response(deduplicate(query('*', **nq),attr="dpaId"),filterfunction=lambda a: True)
        logging.debug("Sector: %s - %s - %s docs" % (k,date.strftime("%Y-%m-%d"),len(res["response"]["docs"])))
        if len(res["response"]["docs"])>0 :
            for d in res["response"]["docs"] :
                for (old,new) in attributeNames.items() :
                    if old in d :
                        d[new]=copy.deepcopy(d[old])
                        del d[old]

            results[k]=res
            results[k]["label"]=n


    for nr in results.values() :
        for doc in nr["response"]["docs"] :
            filename=docfile.format(**locals())e
            doc["document"]=filename
            doc["source"]="ex neoApplication"
            doc["sourcelink"]="javascript:alert('Link für {}')".format(ndoc.get('source',"-"))
            doc["subtitle"]="Untertitel zu {}".format(ndoc.get("title","---"))
            doc["section"]=doc["sections"][0]
            ndoc=copy.deepcopy(doc)
            ndoc["index"]=os.path.join("..",indexfilename)
            ndoc["root"]=os.path.join("..",rootfile)
            texts[os.path.join(directory,filename)]=ndoc
            if textAttribute in doc :
                del(doc[textAttribute])

    with mkdirs_and_open(os.path.join(directory,indexfilename),"w") as of :
        json.dump(dict(news=results,root=rootfile),of)
        logging.info("%s items written to %s" % (reduce(lambda a,b: a+b,
                                                        (len(a["response"]["docs"]) for a in results.values()),0),
                                                 of.name))



for (k,v) in texts.items() :
    json.dump(v,mkdirs_and_open(k,"w"))
logging.debug("%s news objects written" % len(list(texts.keys())))

json.dump(docs,open(os.path.join(directory,rootfile),"w"))



