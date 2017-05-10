# Read in libraries

from bs4 import BeautifulSoup
import requests
import csv
import cookielib, urllib2, sys

# code for simulating a browser -- some websites need this
# from: http://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit/43363447
def doIt(uri):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    page = opener.open(uri)
    page.addheaders = [('User-agent', 'Mozilla/5.0')]
    return page.read()

# initial url to start from 
url = "<REPLACE HERE>"
data = doIt(url) # read data
initSoup = BeautifulSoup(data, "html5lib") # parse
initLinks = initSoup.find_all('a') # find all anchors

###########################################################################################
# STRATEGY
# for each link on the page
#   visit that new page & collect links (and other info) that are there
# Store everything
# In pracitce, we will limit the number of pages that we visit for computational efficiency
# Overall we will have gone 2 steps away from the original page
###########################################################################################

output = []
output.append(["url1","index1","url2","index2","title","date","author"])
allLinks = set()
allLinks.add(url)

count1 = 0 

for initLink in initLinks:   
    if initLink.has_attr('href'):
        if ("#" not in initLink["href"]):
            allLinks.add(initLink)
            index1 = list(allLinks).index(initLink)
            if count1 < 5: #only the top n links
                try:
                    data = doIt(initLink["href"])
                    soup = BeautifulSoup(data, "html5lib")
                    links = soup.find_all('a')
                    title = soup.find("meta",  property="og:title")["content"]   # ensure this is present
                    date = soup.find("time")["datetime"]                         # ensure this is present
                    author = soup.find("meta",  property="og:author")["content"] # ensure this is present
                    count2 = 0
                    for link in links:
                        if (count2 < 5) & link.has_attr('href'):
                            if ("#" not in initLink["href"]):
                                allLinks.add(link)
                                index2 = list(allLinks).index(link)
                                output.append([initLink["href"],index1,link["href"],index2,title,date,author])
                                count1 += 1
                                count2 += 1
                except:
                    pass
