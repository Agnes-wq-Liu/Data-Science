import argparse
import json
import csv
import string
from collections import Counter
import re
#global variables for canonical names
pony_names = {'twilight':'Twilight Sparkle',
              'pinkie':'Pinkie Pie',
              'rarity':'Rarity',
              'rainbow':'Rainbow Dash',
              'fluttershy':'Fluttershy',
              'applejack':'Applejack',
              }

#remove the punctuations
def clean_dialog(dstr):
    translator = str.maketrans('()[],-.?!:;#&',' '*13)#len(string.punctuation))
    return dstr.translate(translator)
def dialog_to_list(dstr):
    return clean_dialog(dstr).strip().split()

#loading input
def load_epi(input_file):
    reader = csv.reader(open(input_file,'r'),quotechar ='"')
    is_header = True
    ed = {}
    ced = {}
    for line in reader:
        if is_header:
            is_header = False
            continue
        episode,writer, pony, dialog = line
        dialog = dialog.lower()
        dialog = dialog_to_list(dialog)
        if pony not in ed.keys():
            ed[pony] = dialog
        else:
            ed[pony].extend(dialog)
    return ed


#making word count output
def compute_word_count(ed):
    grand_output = {}
    #we do for loop for each of the pony:
    for n in ed.keys():
        for i in pony_names.keys():
            if n.lower() == pony_names[i].lower():
                tmp_dict = Counter(ed[n])
                tmp_dict = {i:tmp_dict[i] for i in tmp_dict if tmp_dict[i] >5}
                grand_output[i] =  tmp_dict
    return grand_output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output','-o',required =False, default =None)
    parser.add_argument('input_file')
    args = parser.parse_args()

    episode_dialogs = load_epi(args.input_file)

    word_count = compute_word_count(episode_dialogs)

    output = json.dumps(word_count)

    if args.output is not None:
        with open (args.output,'w') as f:
            f.write(output)
    else:
        print (output)

if __name__ =='__main__':
    main()

