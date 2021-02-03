import numpy
import argparse
import json
import os
import pandas as pd
import re

def make_df(input_file):
    #create dataframe from input file
    try:
        f = open(input_file)
    except Exception:
        print ('cannot open file: file does not exist or incorrect name')
        return None
    key_list =['subreddit','title','name','permalink']    
    lines = f.readlines()
    j = []
    for i in range(len(lines)):
        j.append(json.loads(lines[i]))#load posts into j

    for k in range(len(key_list)):
        this_attribute = []
        for i in range(len(j)):
            try:
                this_attribute.append(j[i][key_list[k]])
            except Exception:
                this_attribute.append(float('NaN'))
        if k == 0:
            df = pd.DataFrame(this_attribute,columns = [key_list[k]])
        else:
            df[key_list[k]] = this_attribute
    df['url'] = ['https://www.reddit.com'+df.loc[i,'permalink']for i in range(df.shape[0])]
    print (df.columns)
    df = df[['subreddit','title','name','url']]    
    
    #adding the column for collect date 
    coll_date = ''
    if '1121' in input_file:
        coll_date = '21'
    elif '1122' in input_file:
        coll_date = '22'
    else:
        coll_date = '23'
    df['collect_date'] = numpy.full((len(lines),1),coll_date)
    return df


def candidate_filter(df):
    #i realized the majority of the posts were outside links so did not bother to consider the contents...
    #only titles
    #we could check for the words surrounded by [\W]s but I found it redundant since in the titles their names are usually surrounded by punctuations and space only
    fdf1 = df[df['title'].str.lower().str.contains('trump')]
    fdf2 = df[df['title'].str.lower().str.contains('biden')]
    fdf = pd.concat([fdf1,fdf2])
    fdf.drop_duplicates(inplace =True)
    return fdf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--out_file',help='out_file')
    parser.add_argument('directory',help='full path to input data directory')
    args = parser.parse_args()
    files = ['20201121_politics.json','20201121_conservative.json','20201122_politics.json','20201122_conservative.json','20201123_politics.json','20201123_conservative.json']
    df = None
    df1 = None
    for f in files:
        this_f= os.path.join(args.directory,f)
        if df is None:
            df = make_df(this_f)
        else:
            df1 = make_df(this_f)
        if df1 is not None:
            df = pd.concat([df,df1])
    filtered_df = candidate_filter(df)
    if args.out_file is not None:
        filtered_df.to_csv(args.out_file,sep ='\t',index = None)
    else:
        print (df)


if __name__=='__main__':
    main()

