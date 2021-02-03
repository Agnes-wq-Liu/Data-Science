import argparse
import requests
from bs4 import BeautifulSoup
import hashlib
import os.path as osp
import json

def get_url_content(cache_dir,url):
    fname = hashlib.sha1(url.encode('utf-8')).hexdigest()
    full_filename = osp.join(cache_dir,fname)
    if not osp.exists(full_filename):
        r = requests.get(url)
        contents = r.text
        with open(full_filename,'w')as f:
            f.write(contents)
    return full_filename


def from_cand_link(candidate_links,name_url):
    relationships = []
    for link in candidate_links:
        if link['href'].startswith('/dating') and link['href']!= name_url:
            relationships.append(link['href'][8:])
    return relationships


def extract_relationships(filename,name_url):
    relationships = []
    soup = BeautifulSoup(open(filename,'r'),'html.parser')
    status_h4 = soup.find('h4','ff-auto-status')
    key_div = status_h4.next_sibling

    candidate_links = key_div.find_all('a')
    
    relationships.extend(from_cand_link(candidate_links,name_url))

    if len(relationships)>1:
        raise Exception('Too many relationships - should have 1')
    
    rl_h4 = soup.find('h4','ff-auto-relationships')
    sib = rl_h4.next_sibling
    while sib is not None and sib.name=='p':
        candidate_links = sib.find_all('a')
        relationships.extend(from_cand_link(candidate_links,name_url))
        sib = sib.next_sibling
    return relationships

 
def saveToOutput(output, final):
    with open(output,'w') as f:
        json.dump(final,f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--config_file',help='config-file.json')
    parser.add_argument('-o','--output_file',help='output_file.json')
    args = parser.parse_args()
    cfile = open(args.config_file,'r')
    config_input = json.load(cfile)
    final  ={}
    cache_dir = osp.join(osp.dirname(__file__),config_input['cache_dir'])

    for x in config_input['target_people']:
        url ='https://www.whosdatedwho.com/dating/{}'.format(x)
        cache_file = get_url_content(cache_dir,url)
        relationships = extract_relationships(cache_file, '/dating/{}'.format(x))
        final[x] = relationships
    if args.output_file is not None:
        saveToOutput(args.output_file,final)
    else:
        print (final)


if __name__=='__main__':
    main()

