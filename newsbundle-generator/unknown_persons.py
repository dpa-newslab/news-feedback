
# coding: utf-8

# In[60]:

from neofonie import query
from collections import defaultdict

unknown=query('*&wt=json&fq=createdAt:[2016-07-22T15:44:39.000Z%20TO%202016-07-23T04:44:39.000Z]&fq=sourceId:"twitter"&facet.mincount=1&fq=labels:"M%C3%BCnchen"&facet=true&facet.field=unknownPersonsSurfaceforms&facet.limit=200&facet.missing=true&f.unknownPersonsSurfaceforms.facet.sort=count&facet.method=enum')
persons=defaultdict(lambda : 0)

personsTable=unknown["facet_counts"]["facet_fields"]['unknownPersonsSurfaceforms']

for i in range(0,len(personsTable),2) :
    persons[str(personsTable[i])]+=personsTable[i+1]



# In[86]:

#exclude based on reguar expressions

import re
exclude = {a for a in persons.keys() if re.search(r"\bGmbh\b",a,re.I) or
                              re.search(r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b",a,re.I) or
                              re.search(r"[:\"]",a) or
                              re.search(r" \. ",a)
}

exclude


# In[67]:

persons.keys()


# In[49]:


specific=query('*Sonboly*&wt=json&fq=createdAt:[2016-07-22T15:44:39.000Z%20TO%202016-07-23T04:44:39.000Z]&fq=sourceId:"twitter"&facet.mincount=1&fq=labels:"M%C3%BCnchen"&facet=true&facet.field=unknownPersonsSurfaceforms&facet.limit=200&facet.missing=true&f.unknownPersonsSurfaceforms.facet.sort=count&facet.method=enum')

specific

