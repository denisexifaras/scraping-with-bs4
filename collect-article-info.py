from bs4 import BeautifulSoup
import requests
import csv
import cookielib, urllib2, sys

def doIt(uri):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    page = opener.open(uri)
    page.addheaders = [('User-agent', 'Mozilla/5.0')]
    return page.read()

url = "<insert outlet main url>"
data = doIt(url)
initSoup = BeautifulSoup(data, "html5lib")
initLinks = initSoup.find_all('a',{"class":"js-headline-text"})
# we have all the links from the main page

# Iterate over all links and save information
articleInfo = []
articleInfo.append(["url","title","date","links","section"])

articleCount = 0
for initLink in initLinks:   
    if initLink.has_attr('href'):
        articleCount += 1
        if articleCount < 50:
            try:        
                data = doIt(initLink["href"])
                soup = BeautifulSoup(data, "html5lib")
                links = str(len(soup.find_all('a')))
                title = soup.find("meta",  property="og:title")["content"]
                date = str(soup.find("time")["datetime"])
                section = soup.find("meta",property="article:section")["content"]
                articleInfo.append([initLink["href"],title,date,links,section])
            except:
                pass

with open('articleInfo.csv', 'w') as f:
    for line in articleInfo:
        tmp = [str(x.encode('utf-8')).replace(",","") for x in line[:-1]]
        tmp.append(str(line[-1]))
        f.write(",".join(tmp) + "\n")


################################################################################
################################################################################
################################################################################
################################################################################

output = []
output.append(["url1","index1","url2","index2"])
allLinks = set()
allLinks.add(url)

for initLink in initLinks:   
    if initLink.has_attr('href'):
        allLinks.add(initLink)
        index1 = list(allLinks).index(initLink)
        try:        
            data = doIt(initLink["href"])
            soup = BeautifulSoup(data, "html5lib")
            links = soup.find_all('a')
            for link in links:
                if link.has_attr('href'):
                    allLinks.add(link)
                    index2 = list(allLinks).index(link)
                    output.append([initLink["href"],index1,link["href"],index2])
                    # print("count2 " + str(count2))
        except:
            pass



with open('articleConnections.csv', 'w') as f:
    for line in output:
        f.write( str(line[1]) + "," + str(line[3]) + "\n")



