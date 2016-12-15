
# coding: utf-8

# # Metadata for URN, newest IDs

# In[33]:

from IPython.core.display import display, HTML
from neofonie import query


def metadata(*urns) :
    result=query(fq=['dpaId:"%s"' % urn for urn in urns],
                 wt="json",
                 omitHeaders=True,
                 q='*',
                 fl='rfc4180,dpaId,dpaTitle'
                 )
    return(result["response"]["docs"])



def newest(sourceId="dpa") :
    result=query(fq=[ "createdAt:[NOW/HOUR-1HOUR TO NOW/HOUR+1HOUR]",
                      'sourceId:"%s"' % sourceId,
                    ],
                 wt="json",
                 omitHeaders=True,
                 q='*',
                 rows=100,
                 sort="createdAt desc",
                 fl='createdAt,dpaId'
                 )
    return(result["response"]["docs"])




docs=newest()

for a in range(0,4) :

    display(HTML("<h3>{dpaTitle}</h3><h6>{dpaId}</h6><pre>{rfc4180}</pre>".format(**(metadata(docs[a]["dpaId"])[0]))))

