import json
import requests
import argparse

def collect(subred):  
    num_posts = 100
    post = []
    last = None
    for i in range(5):
        print (i)
        data = requests.get(f"http://api.reddit.com{subred}/hot?limit={num_posts}&after={last}",
               headers ={'User-Agent':'Agnes Liu'})
        post.extend(data.json()['data']['children'])
        last = data.json()['data']['after']
        print ("post id of current last one in list is",last)
    print (len(post))
    post = post[:500]
    #debug check
    idlst = [post[i]['data']['id'] for i in range(len(post))]
    print (len(list(set(idlst))))
    return post

def write_output(output, post):
    with open (output,'a') as f:
        for y in post:
            json.dump(y,f)
            f.writelines("\n")

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_file',help='output_file')
    parser.add_argument('subreddit',help='subreddit for scraping')
    args = parser.parse_args()
   #remember to handle the situation without output name
   #and include the subreddit for politics
    output = args.output_file
    subred = args.subreddit
    post = collect(subred)
    write_output(output,post)


if __name__ =='__main__':
    main()

