import pandas as pd
import re
import json
from decimal import *
import operator
import heapq
import os.path as osp
import argparse
import sys
from hw3.functions import *
script_dir = osp.dirname(__file__)
#export PYTHONPATH=/root/comp598_ds/HW3_260713093/src:$PYTHONPATH    

#******************************************main function*******************************************#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='path to input; the input file should be a csv file (clean_dialog.csv)')
    parser.add_argument('-o','--op', help='output file name')
    args = parser.parse_args()

    mlp = pd.read_csv(args.input_path)
    spkr_names = patterns()
    data = os.path.join(os.path.dirname(__file__), '..','data','words_alpha.txt')
    verb = verbose(mlp)
    print ("finished counting verbosity")
    ment = mention(mlp)
    print ("finished counting mention times")
    follow = follow_on_comment(mlp)
    print ("finished counting follow_on comments")
    
    nondict = non_dict(data,mlp)
    print ("finished counting non dictionary words")
    jsonobj = {}
    jsonobj["verbosity"] = verb 
    jsonobj["mentions"] = ment
    jsonobj["follow_on_comments"] = follow
    jsonobj["non_dictionary_words"] = nondict
#   if given an output name, write to this file
    if args.op is None:
        #print (json.dumps(jsonobj))
        print (jsonobj)
    else:
        with open (args.op,"w") as f:
            json.dump(jsonobj,f)
    #else, write JSON output to stdout
    
if __name__ == '__main__':
    main()

