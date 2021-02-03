import pandas as pd
import re
import json
from decimal import *
import operator
import heapq
import os.path
import argparse
import sys

#**************************************************helpers******************************************************#

# define patterns
def patterns():
    t = re.compile('T(?i)wilight+\ +S(?i)parkle')
    a = re.compile('A(?i)pplejack')
    r = re.compile('R(?i)arity')
    p = re.compile('P(?i)inkie+\ +P(?i)ie')
    rd = re.compile('R(?i)ainbow+\ +D(?i)ash')
    f = re.compile('F(?i)luttershy')
    spkr_names =[t,a,r,p,rd,f]
    return spkr_names
#create speaker names as global variable
spkr_names = patterns()

# index patterns
def compName(i):
    if i==0:
        return 'twilight sparkle'
    if i==1:
        return 'applejack'
    if i==2:
        return 'rarity'
    if i==3:
        return 'pinkie pie'
    if i==4:
        return 'rainbow dash'
    if i==5:
        return 'fluttershy'
# get list of name words by index
def getname(i):
    name0 = ['Twilight','Sparkle']
    name1 = ['Applejack']
    name2 = ['Rarity']
    name3 = ['Pinkie','Pie']
    name4 = ['Rainbow','Dash']
    name5 = ['Fluttershy']
    if (i==0):
        return name0
    elif (i==1) :
        return name1
    elif (i==2) :
        return name2
    elif (i==3) :
        return name3
    elif (i==4) :
        return name4
    else :
        return name5
    
#from int to names appearing on JSON
def intToName(i):
    name0 = "twilight"
    name1 = "applejack"
    name2 = "rarity"
    name3 = "pinkie"
    name4 = "rainbow"
    name5 = "fluttershy"
    name6 = "other"
    if (i==0):
        return name0
    elif (i==1) :
        return name1
    elif (i==2) :
        return name2
    elif (i==3) :
        return name3
    elif (i==4) :
        return name4
    elif (i==5):
        return name5
    else:
        return name6

#   get subset with pony speechacts
def with_pony(mlp,p):
    spkr_names = patterns()
    ponies = mlp[mlp["pony"].str.lower()==compName(p)]
    return ponies
             


# *********************************************************verbosity***************************************************#
#speech act of each pony alone, divided by speech in total

def cnt_sa(mlp,p):
    spkr_names = patterns()
    #if consecutive within same title, count as 1
    cnt = 0
    prev = ""
    prev_t =""
    name = spkr_names[p]
    for index, row in mlp.iterrows():
        # count the speech act of each pony
        if(re.match(name,prev) and (row.values[2]==prev)):
            if prev_t ==row.values[0]:
                continue
            else:
                cnt+=1
        elif((not re.match(name,prev)) and re.match(name,row.values[2])):
            cnt+=1                   
        prev = row.values[2]
        prev_t = row.values[0]
    return cnt

def verbose(mlp):
    tsa = 0
    nums = [0,0,0,0,0,0]
    percent = [0,0,0,0,0,0]
    otr = 1
    for i in range(0,6,1):
        nums[i] = cnt_sa(mlp,i)
        tsa+=nums[i]
    for i in range(0,6,1):
        percent[i] = nums[i]/tsa
        otr-=percent[i]
        percent[i] = float (Decimal(percent[i]).quantize(Decimal('.01')))

    verb = {intToName(i):percent[i] for i in range(0,6,1)}
    return verb



#**********************************************************mentions*********************************************************#


def mention_single(mlp,p):
    spkr_names = patterns()
    ment = with_pony(mlp,p)
    p_list = [intToName(i) for i in range (0,6,1)]
    cnt = [0,0,0,0,0,0]
    for i in range (0,6,1):
        name = getname(i)
        full_name = ' '.join(name)
        if len(name)==1:
            cnt[i]+=sum(ment.dialog.str.count(name[0]).values)
        else:
            for z in name:
                cnt[i]+=sum(ment.dialog.str.count(z).values)
            cnt[i]-=sum(ment.dialog.str.count(full_name).values)
    total = sum(cnt)-cnt[p]
    if total==0:
        return {}
    else:
        p_list.pop(p)
        cnt.pop(p)
        tp_ment= {p_list[i]:float(Decimal(cnt[i]/total).quantize(Decimal('.01'))) for i in range(0,5,1)}
        return tp_ment

def mention(mlp):
    spkr_names = patterns()
    for i in range(0,6,1):
        tmp_dict = mention_single(mlp,i)
        if i==0:
            mention_dict = {intToName(i):tmp_dict}    
        else:
            mention_dict[intToName(i)] = tmp_dict
    return mention_dict


#*********************************************************follow on comments ***************************************#

def follow_on(mlp,p):
    spkr_names = patterns()
    # get subset with all pony speech acts
    p_list = list(range(0,6))
    cnt = [0,0,0,0,0,0]
    this_pony = 0
    for index, row in mlp.iterrows():
        if index ==0:
            continue 
            #don't check the first series
        elif not(re.match(spkr_names[p],row.values[2])):
            continue
        else:
            this_pony+=1
            for i in p_list:
                if (re.match(spkr_names[i],mlp.iloc[index-1,2])) and (row.values[0]==mlp.iloc[index-1,0]):
                    cnt[i] +=1
            # if this.pony isn't the given pony then continue
    cnt.append(this_pony-sum(cnt))
    p_list.append(6)
    cnt.pop(p)
    p_list.pop(p)
    total = sum(cnt)
    if total==0:
        return {}
    else:
        this_followon = {intToName(p_list[i]):float(Decimal(cnt[i]/total).quantize(Decimal('.01'))) for i in range(0,6,1)}
        return this_followon

def follow_on_comment(mlp):
    spkr_names = patterns()
    for i in range(0,6,1):
        tmp_dict = follow_on(mlp,i)
        if i==0:
            foc_dict = {intToName(i):tmp_dict}
        else:
            foc_dict[intToName(i)] = tmp_dict
    return foc_dict

#********************************************************Non_dictionary words*********************************************#


# write a function for 1 pony and call for all of them
def non_dict_p(word_dict, mlp,p):
    non_dict = {line.strip('\n') for line in open(word_dict)}

    # first filter all the words
    this_pony = with_pony(mlp,p)
    atpl= list(this_pony.dialog.str.split())
    atpl = sum(atpl,[])
    atpl = list( dict.fromkeys(atpl) )#remove duplicants
    atpl = ' '.join (atpl)
    atpl = re.sub(r'\<U\++[\w]+\>',' ',atpl)
#     print (atpl)
    ndtpl = re.findall(r"[\w]+", atpl)#remove symbols
    ndtpl = {x.lower() for x in ndtpl}
    temp1 = ndtpl.intersection(non_dict)
    nd = ndtpl-temp1
    # print (len(nd))

    nd = list(nd)
    the_count = []
    for x in nd:
        if the_count==[]:
            the_count = [this_pony.dialog.str.count(x).sum()]
        else:
            the_count.append(this_pony.dialog.str.count(x).sum())

    nd_cnt_dict=dict(zip(nd,the_count))

    max_cnts=list(heapq.nlargest(5, nd_cnt_dict, key=nd_cnt_dict.get))
    return max_cnts

def non_dict(word_dict,mlp):
    counts = []
    k= []
    for i in range (0,6,1):
        if counts==[]:
            counts= [non_dict_p(word_dict,mlp,i)]
            k = [intToName(i)]
        else:
            counts.append(non_dict_p(word_dict,mlp,i))
            k.append(intToName(i))
    non_dict = dict(zip(k,counts))
    return non_dict
