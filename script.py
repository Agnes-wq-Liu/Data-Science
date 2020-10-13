#Agnes Liu 260713093 COMP598 A1 script
import pandas as pd
import re
from decimal import *
# 1. data collection
# select first 10,000 tweets in English without question
twt = pd.read_csv("/root/comp598_ds/IRAhandle_tweets_1.csv")
twt = twt[:10000]
twt = twt[twt['language']=='English']
for x in twt.index:
    if('?' in twt.loc[x,'content']):
        twt.drop(x,inplace =True)

# 2. data annotation: add feature trump_mention, then select columns: tweet_id, publish_date, content, trump_mention
contain_Trump = []
# p1 = re.compile('[\W]+T[Rr][Uu][Mm][Pp]+[\W]')
p1 = re.compile('[\W]+T(?i)rump+[\W]')
for x in twt.index:
    text = twt.loc[x,'content']
    if((re.search(p1,text) != None) or ((text.startswith('T(?i)rump')) or (text.endswith('T(?i)rump')))):
        if (contain_Trump==[]):
            contain_Trump=['T']
        else:
            contain_Trump.append('T')
    else:
        if (contain_Trump==[]):
            contain_Trump=['F']
        else:
            contain_Trump.append('F')
            

twt['trump_mention'] = contain_Trump
twt = twt[['tweet_id', 'publish_date', 'content','trump_mention']]
# save the file
twt.to_csv("/root/comp598_ds/dataset.tsv", index =None, sep = '\t')

# 3. data analysis
# fraction of tweets mentioned Trump
ctTr = 0
nTr = 0
for x in contain_Trump:
    if (x=='T'):
        ctTr+=1;
    else:
        nTr+=1;
print(ctTr, nTr)

quotient = float(ctTr/(ctTr+nTr))
q = str(Decimal(quotient).quantize(Decimal('.001')))
print(q)


# save the file
with open("/root/comp598_ds/results.tsv","w") as f:
    f.write("result"+'\t'+"value"+'\n')
    f.write("frac-trump-mentions" + '\t'+q)
