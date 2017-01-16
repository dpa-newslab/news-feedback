# -*- coding: utf-8 -*-
"""

@author: martin virtel
"""

import re
import sys
import logging
import pipe
import copy

logging.basicConfig(level=logging.DEBUG,stream=sys.stderr)
logger=logging.getLogger(__name__)



@pipe.Pipe
def deduplicate(iterable,key=lambda a : hash(a)) :
    """
     deduplicate iterable: filter all but the first ocurrence of key(item)
     key(item) has to be hashable.
     a sequence of [("a",1),("b",2),("c",3),("a",5)] can be deduplicated using lambda a: a[0]
     it would be converted to  [("a",1),("b",2),("c",3)].
    """
    already=set()
    for item in iterable :
        k=key(item)
        if k not in already :
            already.add(k)
            yield item

@pipe.Pipe
def rename_attributes(iterable,pairs) :
    for item in iterable :
        for (on,nn) in pairs :
            if on in item :
                item[nn]=copy.deepcopy(item[on])
                # logger.debug("renamed {} -> {} {}".format(on,nn,item[nn]))
                del item[on]
        yield item


@pipe.Pipe
def default_attributes(iterable,attrlist,value="") :
    for item in iterable :
        for a in attrlist :
            if a not in item :
                item[a]=value
        yield item



def test_deduplicate() :
    import copy
    doc=[{'body': 'b', 'title': 'a'},
         {'body': 'c', 'title': 'a'}]

    # based on attr
    assert(list(copy.deepcopy(doc) | deduplicate(key=lambda a: a["title"]))==
        [{'body': 'b', 'title': 'a'}])

def test_rename_attributes() :
    assert(list([{ 'a' : 1 }] | rename_attributes([('a','b')]))==
            [{'b' : 1 }])



if __name__=='__main__' :
    from pprint import pprint
    test_deduplicate()
    test_rename_attributes()

