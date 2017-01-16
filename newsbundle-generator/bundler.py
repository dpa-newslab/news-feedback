
# coding: utf-8
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
            res=list(neofonie.query("*",**nq)["response"]["docs"] | datapipeline.rename_attributes(config.rename)
                    | pipe.where(config.filter)
                    | datapipeline.deduplicate(key=lambda a: a["title"] )
                    | datapipeline.default_attributes(('sourcelink','source','subtitle'))
                )
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
    t=copy.deepcopy(config.template)
    t["chapters"]=docs
    json.dump(t,open(os.path.join(config.directory,config.rootfile),"w"))



def test() :
    pass


if __name__ == "__main__" :
    test()

