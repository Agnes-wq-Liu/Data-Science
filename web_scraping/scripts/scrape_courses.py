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


def splitFields(title):
    title = title.split(' ')
    cid = title[0]+' '+title[1]
    cn = ' '.join(title[2:-2])
    cr = title[-2].strip('(')
    return cid,cn,cr

def extract(cache_dir,url):
    filename = get_url_content(cache_dir,url)
    cid = []
    cn = []
    cr = []
    content = []
    soup = BeautifulSoup(open(filename,'r'),'html.parser')
    div = soup.find('div','view-content')
    alist = div.find_all('a')
    for a in alist:
        content.append(a.contents[0])
    for c in content:
        cidtmp,cntmp,crtmp = splitFields(str(c))
        cid.append(cidtmp)
        cn.append(cntmp)
        cr.append(crtmp)
    return cid,cn,cr

 
def printToOutput(cId,cN,cr):
    print ('CourseID, Course Name, # of credits')
    for i in range(len(cId)):
        try:
            x = int(cr[i])
            print(cId[i]+',',cN[i]+',',cr[i])
        except Exception:
            continue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--caching_dir',help='caching directory')
    parser.add_argument('page',help='page #')
    args = parser.parse_args()
    url = 'https://www.mcgill.ca/study/2020-2021/courses/search?page='+args.page
    cache_dir = args.caching_dir
    courseId, courseName, credit = extract(cache_dir, url)
    printToOutput(courseId, courseName, credit)


if __name__=='__main__':
    main()

