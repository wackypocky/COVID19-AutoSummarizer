
import urllib
import requests
from bs4 import BeautifulSoup
import os
import re
import sys

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

"""
Scrape function. Returns a list of search result items. Each item is a dict with keys "title" and "link".
"""
def scrapeGoogle(query, max):
    query = urllib.parse.quote_plus(query) # Format into URL encoding
    number_result = max # how many results we want
    headers = {"user-agent" : USER_AGENT}

    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    resp = requests.get(google_url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

    result_div = soup.find_all('div', attrs = {'class': 'r'})

    results=[]
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            anchors = r.find_all('a')
            if anchors:
                # print("type of anchors:", type(anchors))
                for anchor in anchors:
                    link = anchor.get('href')
                    title = anchor.find('h3', class_="LC20lb DKV0Md").get_text()

                    # Check to make sure everything is present before appending
                    if link != '' and title != '':
                        item = {
                            "title": title,
                            "link": link
                        }
                        results.append(item)
        # Next loop if one element is not present
        except:
            continue
    return results

"""
Main function.
"""
def main():
    myquery = sys.argv[1]
    max_queries = sys.argv[2]
    results = scrapeGoogle(myquery, max_queries)

    headers = {"user-agent" : USER_AGENT}
    token = "5eecec4767199486a01962f7dbf05e30"
    print("results:", results)
    for item in results:
        encoded_url = urllib.parse.quote(item['link'])
        url = "https://api.diffbot.com/v3/article?token=" + token + "&url=" + encoded_url
        resp = requests.get(url=url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            objects = data['objects']
            for object in objects:
                title = object['title']

                # save the objects array for future use
                obj_filename = 'objects/'+title.replace(" ", '')+".txt"
                with open(obj_filename, 'w') as f:
                    f.write(title + '\n')
                    f.write(str(objects))

                text = object['text']
                if 'date' in object:
                    date = object['date']
                elif 'estimatedDate' in object:
                    date = object['estimatedDate']
                else:
                    date = 'n/a'

                # get tags and analysis!
                tag_info = []
                if 'tags' in object:
                    tags = object['tags']
                    for tag in tags:
                        tag_info.append(tag['label'] + "_" + str(tag['count']) + "_" + str(tag['score']))
                else:
                    tag_info = 'n/a'

                if 'publisherRegion' in object:
                    region = object['publisherRegion']
                else:
                    region = 'n/a'

                # remove spaces from title for filename
                filename = "articles/" + title.replace(" ", '') + ".txt"
                with open(filename, 'w') as f:
                    f.write(title + "\n")
                    f.write(date + "\n")
                    f.write(region + "\n")
                    f.write(str(tag_info)+'\n')
                    f.write(text)

        # resp = requests.get(url=item['link'], headers=headers)
        # if resp.status_code == 200:
        #     soup = BeautifulSoup(resp.content, "html.parser")
        #     # print(soup)
        #     body = soup.find("body")
        #     title = body.title
        #     if title:
        #         title = title.string
        #         if not title:
        #             title = item['title']
        #         else:
        #             title = title.replace('\r', '')
        #             if not title:
        #                 title = item['title']
        #             else:
        #                 title = title.replace('\n', '')
        #                 if not title:
        #                     title = item['title']
        #                 else:
        #                     title = title.replace('\t', '')
        #                     if not title:
        #                         title = item['title']
        #                     else:
        #                         title = title.strip()
        #                         if not title:
        #                             title = item['title']
        #
        #     else:
        #         title = item['title']
        #     text = body.find_all(text=True)
        #
        #     html_filename = 'html/'+title.replace(" ", '')+".txt"
        #     with open(html_filename, 'w') as f:
        #         f.write(title)
        #         f.write(str(body))
        #
        #     output = ''
        #     blacklist = [
        #         '[document]',
        #         'noscript',
        #         'header',
        #         'html',
        #         'meta',
        #         'head',
        #         'input',
        #         'script',
        #         'style',
        #         'footer',
        #         'span',
        #         # there may be more elements you don't want, such as "style", etc.
        #     ]
        #     for t in text:
        #         if t.parent.name not in blacklist:
        #             match = re.search('<!--', t)
        #             if match:
        #                 continue
        #             output += '{} '.format(t)
        #     # for chunk in article:
        #     #     text = chunk.find_all(string=True)
        #         # blacklist = [
        #         # 	'[document]',
        #         # 	'noscript',
        #         # 	'header',
        #         # 	'html',
        #         # 	'meta',
        #         # 	'head',
        #         # 	'input',
        #         # 	'script',
        #         #     'style',
        #         #     'footer',
        #         #     'span',
        #         # 	# there may be more elements you don't want, such as "style", etc.
        #         # ]
        #         # for t in text:
        #         # 	if t.parent.name not in blacklist:
        #         # 		output += '{} '.format(t)
        #
        #     # remove extra newlines/spaces
        #     lines = output.split('\n')
        #     article = ''
        #     for line in lines:
        #         if line != '':
        #             temp = line.strip()
        #             if temp:
        #                 article += temp + '\n'

if __name__ == '__main__':
    main()
