import argparse
import json
import math
#return the tf-idf score of each word

def compute_tfidf(filename):
    #read the file as dictionary and perform calculation
    output = {}
    #compute the num of words
    f = open (filename, 'r')
    pony_count = json.load(f)
    nwords = 0
    for p in pony_count.keys():
        nwords += sum(pony_count[p].values())
        
    for p in pony_count.keys():
        pony = {}
        for k in pony_count[p].keys():
            #for each word of the pony
            #first, get freq(word)
            fword = sum(pony_count[i][k] for i in pony_count.keys() if k in pony_count[i].keys())
            #then, get freq(w|p)
            fwp = pony_count[p][k]
            tfidf = fwp*math.log(nwords/fword)
            pony[k] = tfidf
        output[p] = pony
    return output


def sort_n_filter(output,n):
    newout = {}
    for p in output.keys():
        tmp = output[p]
        tmp = {k:tmp[k] for k in sorted(tmp,key = tmp.get,reverse =True)}
        tmp = {k:tmp[k] for k in list(tmp.keys())[:int(n)]}
        newout[p] = list(tmp.keys())
    return newout

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input',help='<pony_counts.json>')
    parser.add_argument('num_words',help='number of wanted words per pony')
    args = parser.parse_args()
    output = compute_tfidf(args.input)
    output = sort_n_filter(output,args.num_words)
    print (output)
if __name__ =='__main__':
    main()

